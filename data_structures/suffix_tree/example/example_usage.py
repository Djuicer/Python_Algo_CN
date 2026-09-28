#  Created by: Ramy-Badr-Ahmed (https://github.com/Ramy-Badr-Ahmed)
#  在 Pull Request: #11554
#  https://github.com/TheAlgorithms/Python/pull/11554
#
#  Please mention me (@Ramy-Badr-Ahmed) 在 任意 问题 或 pull request
#  寻址 bugs/corrections 到 此 文件。
#  Thank you!

from data_structures.suffix_tree.suffix_tree import SuffixTree


def main() -> None:
    """
    Demonstrate usage 的 SuffixTree 类。

    - Initializes SuffixTree 带有 predefined 文本。
    - Defines 一个列表 的 patterns 到 搜索 之内 后缀 树。
    - 搜索 每个 模式 在 后缀 树。

    Patterns tested:
        - "ana" (找到) --> True
        - "ban" (找到) --> True
        - "na" (找到) --> True
        - "xyz" (未找到) --> False
        - "mon" (找到) --> True
    """
    text = "monkey banana"
    suffix_tree = SuffixTree(text)

    patterns = ["ana", "ban", "na", "xyz", "mon"]
    for pattern in patterns:
        found = suffix_tree.search(pattern)
        print(f"Pattern '{pattern}' found: {found}")


if __name__ == "__main__":
    main()
