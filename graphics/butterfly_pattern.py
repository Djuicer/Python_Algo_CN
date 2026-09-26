def butterfly_pattern(n: int) -> str:
    """
    创建大小为 n 的蝴蝶图案，并以字符串形式返回。

    >>> print(butterfly_pattern(3))
    *   *
    ** **
    *****
    ** **
    *   *
    >>> print(butterfly_pattern(5))
    *       *
    **     **
    ***   ***
    **** ****
    *********
    **** ****
    ***   ***
    **     **
    *       *
    """
    result = []

    # 上半部分
    for i in range(1, n):
        left_stars = "*" * i
        spaces = " " * (2 * (n - i) - 1)
        right_stars = "*" * i
        result.append(left_stars + spaces + right_stars)

    # 中间部分
    result.append("*" * (2 * n - 1))

    # 下半部分
    for i in range(n - 1, 0, -1):
        left_stars = "*" * i
        spaces = " " * (2 * (n - i) - 1)
        right_stars = "*" * i
        result.append(left_stars + spaces + right_stars)

    return "\n".join(result)


if __name__ == "__main__":
    n = int(input("Enter the size of the butterfly pattern: "))
    print(butterfly_pattern(n))
