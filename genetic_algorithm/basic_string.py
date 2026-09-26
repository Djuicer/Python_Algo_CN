"""
用于展示遗传算法（Genetic Algorithm）四个阶段如何工作的简单多线程算法：
评估（Evaluation）、选择（Selection）、交叉（Crossover）和变异（Mutation）。
https://en.wikipedia.org/wiki/Genetic_algorithm
Author: D4rkia
"""

from __future__ import annotations

import random

# 种群的最大规模。规模越大可能越快，但会占用更多内存
N_POPULATION = 200
# 每一代进化中选出的元素数量。按当代适应度从高到低选择，且必须小于 N_POPULATION
N_SELECTED = 50
# 一代中某个元素发生变异（改变其中一个基因）的概率
# 这将保证进化过程中会使用所有基因
MUTATION_PROBABILITY = 0.4
# 仅用于增强算法所需随机性的种子
random.seed(random.randint(0, 1000))


def evaluate(item: str, main_target: str) -> tuple[str, float]:
    """
    通过统计位置正确的字符数量，评估 item 与 target 的相似程度。
    >>> evaluate("Helxo Worlx", "Hello World")
    ('Helxo Worlx', 9.0)
    """
    score = len([g for position, g in enumerate(item) if g == main_target[position]])
    return (item, float(score))


def crossover(parent_1: str, parent_2: str) -> tuple[str, str]:
    """
    在随机位置切分并组合两个字符串。
    >>> random.seed(42)
    >>> crossover("123456", "abcdef")
    ('12345f', 'abcde6')
    """
    random_slice = random.randint(0, len(parent_1) - 1)
    child_1 = parent_1[:random_slice] + parent_2[random_slice:]
    child_2 = parent_2[:random_slice] + parent_1[random_slice:]
    return (child_1, child_2)


def mutate(child: str, genes: list[str]) -> str:
    """
    从列表中选择另一个基因，替换子代的一个随机基因以完成变异。
    >>> random.seed(123)
    >>> mutate("123456", list("ABCDEF"))
    '12345A'
    """
    child_list = list(child)
    if random.uniform(0, 1) < MUTATION_PROBABILITY:
        child_list[random.randint(0, len(child)) - 1] = random.choice(genes)
    return "".join(child_list)


    # 对新种群执行选择、交叉和变异
def select(
    parent_1: tuple[str, float],
    population_score: list[tuple[str, float]],
    genes: list[str],
) -> list[str]:
    """
    选择第二个亲本并生成新种群。

    >>> random.seed(42)
    >>> parent_1 = ("123456", 8.0)
    >>> population_score = [("abcdef", 4.0), ("ghijkl", 5.0), ("mnopqr", 7.0)]
    >>> genes = list("ABCDEF")
    >>> child_n = int(min(parent_1[1] + 1, 10))
    >>> population = []
    >>> for _ in range(child_n):
    ...     parent_2 = population_score[random.randrange(len(population_score))][0]
    ...     child_1, child_2 = crossover(parent_1[0], parent_2)
    ...     population.extend((mutate(child_1, genes), mutate(child_2, genes)))
    >>> len(population) == (int(parent_1[1]) + 1) * 2
    True
    """
    pop = []
        # 按适应度分数成比例地生成更多子代
    child_n = int(parent_1[1] * 100) + 1
    child_n = 10 if child_n >= 10 else child_n
    for _ in range(child_n):
        parent_2 = population_score[random.randint(0, N_SELECTED)][0]

        child_1, child_2 = crossover(parent_1[0], parent_2)
            # 将新字符串加入种群列表
        pop.append(mutate(child_1, genes))
        pop.append(mutate(child_2, genes))
    return pop


def basic(target: str, genes: list[str], debug: bool = True) -> tuple[int, int, str]:
    """
    验证 target 不包含 genes 变量所列基因以外的基因。

    >>> from string import ascii_lowercase
    >>> basic("doctest", ascii_lowercase, debug=False)[2]
    'doctest'
    >>> genes = list(ascii_lowercase)
    >>> genes.remove("e")
    >>> basic("test", genes)
    Traceback (most recent call last):
        ...
    ValueError: ['e'] is not in genes list, evolution cannot converge
    >>> genes.remove("s")
    >>> basic("test", genes)
    Traceback (most recent call last):
        ...
    ValueError: ['e', 's'] is not in genes list, evolution cannot converge
    >>> genes.remove("t")
    >>> basic("test", genes)
    Traceback (most recent call last):
        ...
    ValueError: ['e', 's', 't'] is not in genes list, evolution cannot converge
    """

    # 验证 N_POPULATION 是否大于 N_SELECTED
    if N_POPULATION < N_SELECTED:
        msg = f"{N_POPULATION} must be bigger than {N_SELECTED}"
        raise ValueError(msg)
    # 验证 target 不包含 genes 变量所列基因以外的基因
    not_in_genes_list = sorted({c for c in target if c not in genes})
    if not_in_genes_list:
        msg = f"{not_in_genes_list} is not in genes list, evolution cannot converge"
        raise ValueError(msg)

    # 生成随机初始种群
    population = []
    for _ in range(N_POPULATION):
        population.append("".join([random.choice(genes) for i in range(len(target))]))

    # 输出一些日志，以了解算法的运行情况
    generation, total_population = 0, 0

    # 找到与目标完全匹配的结果后结束此循环
    while True:
        generation += 1
        total_population += len(population)

        # 随机种群已创建，现在开始评估

        # （方案 1）加入少量并发可以加快整体速度，
        #
        # import concurrent.futures
        # population_score: list[tuple[str, float]] = []
        # with concurrent.futures.ThreadPoolExecutor(
        #                                   max_workers=NUM_WORKERS) as executor:
        #     futures = {executor.submit(evaluate, item, target) for item in population}
        #     concurrent.futures.wait(futures)
        #     population_score = [item.result() for item in futures]
        #
        # 但对于这种简单算法，反而可能更慢
        # （方案 2）只需对种群中的每个元素调用 evaluate
        population_score = [evaluate(item, target) for item in population]

        # 检查是否出现匹配的进化结果
        population_score = sorted(population_score, key=lambda x: x[1], reverse=True)
        if population_score[0][0] == target:
            return (generation, total_population, population_score[0][0])

        # 每 10 代输出一次最佳结果，以确认算法正在运行
        if debug and generation % 10 == 0:
            print(
                f"\nGeneration: {generation}"
                f"\nTotal Population:{total_population}"
                f"\nBest score: {population_score[0][1]}"
                f"\nBest string: {population_score[0][0]}"
            )

        # 清除旧种群，同时保留部分最佳进化结果，以避免进化倒退
        population_best = population[: int(N_POPULATION / 3)]
        population.clear()
        population.extend(population_best)
        # 将种群分数归一化到 0 和 1 之间
        population_score = [
            (item, score / len(target)) for item, score in population_score
        ]

        # 执行选择
        for i in range(N_SELECTED):
            population.extend(select(population_score[int(i)], population_score, genes))
        # 检查种群是否已达到最大规模，若是则跳出循环。若禁用此检查，算法处理
        # 长字符串时会耗时极久，但计算短字符串所需代数也会少得多
            if len(population) > N_POPULATION:
                break


if __name__ == "__main__":
    target_str = (
        "This is a genetic algorithm to evaluate, combine, evolve, and mutate a string!"
    )
    genes_list = list(
        " ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklm"
        "nopqrstuvwxyz.,;!?+-*#@^'èéòà€ù=)(&%$£/\\"
    )
    generation, population, target = basic(target_str, genes_list)
    print(
        f"\nGeneration: {generation}\nTotal Population: {population}\nTarget: {target}"
    )
