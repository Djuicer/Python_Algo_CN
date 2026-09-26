"""
给定一个任务列表，每个任务都有截止期限和收益，计算应完成哪些任务才能获得
最大收益。每个任务需要一个单位时间，并且同一时间只能处理一个任务。任务一旦
超过截止期限，就无法再安排。

示例：
tasks_info = [(4, 20), (1, 10), (1, 40), (1, 30)]
max_tasks 将返回 (2, [2, 0])——安排这些任务可获得 40 + 20 的收益。

该问题可使用贪心算法（Greedy Algorithm）求解。
时间复杂度——O(n log n)
https://medium.com/@nihardudhat2000/job-sequencing-with-deadline-17ddbb5890b5
"""

from dataclasses import dataclass
from operator import attrgetter


@dataclass
class Task:
    task_id: int
    deadline: int
    reward: int


def max_tasks(tasks_info: list[tuple[int, int]]) -> list[int]:
    """
    创建 Task 对象列表，并按收益从高到低排序。
    返回能够在 i 变得过大之前完成的任务 ID 列表。
    >>> max_tasks([(4, 20), (1, 10), (1, 40), (1, 30)])
    [2, 0]
    >>> max_tasks([(1, 10), (2, 20), (3, 30), (2, 40)])
    [3, 2]
    >>> max_tasks([(9, 10)])
    [0]
    >>> max_tasks([(-9, 10)])
    []
    >>> max_tasks([])
    []
    >>> max_tasks([(0, 10), (0, 20), (0, 30), (0, 40)])
    []
    >>> max_tasks([(-1, 10), (-2, 20), (-3, 30), (-4, 40)])
    []
    """
    tasks = sorted(
        (
            Task(task_id, deadline, reward)
            for task_id, (deadline, reward) in enumerate(tasks_info)
        ),
        key=attrgetter("reward"),
        reverse=True,
    )
    return [task.task_id for i, task in enumerate(tasks, start=1) if task.deadline >= i]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print(f"{max_tasks([(4, 20), (1, 10), (1, 40), (1, 30)]) = }")
    print(f"{max_tasks([(1, 10), (2, 20), (3, 30), (2, 40)]) = }")
