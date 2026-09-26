def gray_code(bit_count: int) -> list[int]:
    """
    接收整数 n，返回 n 位格雷码序列。
    n 位格雷码序列由 2^n 个整数组成，其中：

    a) 每个整数均位于闭区间 [0,2^n -1] 内
    b) 序列以 0 开头
    c) 每个整数在序列中至多出现一次
    d) 每对相邻整数的二进制表示恰好有一位不同
    e) 首尾两个整数的二进制表示也恰好有一位不同

    >>> gray_code(0)
    [0]

    >>> gray_code(2)
    [0, 1, 3, 2]

    >>> gray_code(1)
    [0, 1]

    >>> gray_code(3)
    [0, 1, 3, 2, 6, 7, 5, 4]

    >>> gray_code(-1)
    Traceback (most recent call last):
        ...
    ValueError: The given input must be positive

    >>> gray_code(10.6)
    Traceback (most recent call last):
        ...
    TypeError: unsupported operand type(s) for <<: 'int' and 'float'
    """

    # bit_count 表示格雷码的位数
    if bit_count < 0:
        raise ValueError("The given input must be positive")

    # 获取生成的字符串序列并将其转换为整数
    sequence = gray_code_sequence_string(bit_count)
    return [int(code, 2) for code in sequence]


def gray_code_sequence_string(bit_count: int) -> list[str]:
    """
    以位字符串形式输出 n 位格雷码序列。

    >>> gray_code_sequence_string(0)
    ['0']

    >>> gray_code_sequence_string(2)
    ['00', '01', '11', '10']

    >>> gray_code_sequence_string(1)
    ['0', '1']
    """

    # 使用递归方法
    # n = 0 或 n = 1 时到达基本情况
    if bit_count == 0:
        return ["0"]

    if bit_count == 1:
        return ["0", "1"]

    seq_len = 1 << bit_count  # 定义序列长度
    # 1 << n 等价于 2^n

    # 递归生成 n - 1 位的结果
    smaller_sequence = gray_code_sequence_string(bit_count - 1)

    sequence: list[str] = []

    # 在生成的较短序列前半部分前添加 0
    for i in range(seq_len // 2):
        generated_no = "0" + smaller_sequence[i]
        sequence.append(generated_no)

    # 从列表末尾开始，在后半部分前添加 1
    for i in reversed(range(seq_len // 2)):
        generated_no = "1" + smaller_sequence[i]
        sequence.append(generated_no)

    return sequence


if __name__ == "__main__":
    import doctest

    doctest.testmod()
