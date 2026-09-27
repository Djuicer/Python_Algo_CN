"""
这是使用纯 Python 实现的斐波那契数列动态规划（Dynamic Programming）解法。
"""


class Fibonacci:
    def __init__(self) -> None:
        self.sequence = [0, 1]

    def get(self, index: int) -> list:
        """
        获取索引为 `index` 的斐波那契数。如果该数尚不存在，
        则计算直至索引 `index` 之前所有缺少的数。

        >>> Fibonacci().get(10)
        [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
        >>> Fibonacci().get(5)
        [0, 1, 1, 2, 3]
        """
        if (difference := index - (len(self.sequence) - 2)) >= 1:
            for _ in range(difference):
                self.sequence.append(self.sequence[-1] + self.sequence[-2])
        return self.sequence[:index]


def main() -> None:
    print(
        "Fibonacci Series Using Dynamic Programming\n",
        "Enter the index of the Fibonacci number you want to calculate ",
        "in the prompt below. (To exit enter exit or Ctrl-C)\n",
        sep="",
    )
    fibonacci = Fibonacci()

    while True:
        prompt: str = input(">> ")
        if prompt in {"exit", "quit"}:
            break

        try:
            index: int = int(prompt)
        except ValueError:
            print("Enter a number or 'exit'")
            continue

        print(fibonacci.get(index))


if __name__ == "__main__":
    main()
