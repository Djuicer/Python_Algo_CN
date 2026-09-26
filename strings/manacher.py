def palindromic_string(input_string: str) -> str:
    """
    >>> palindromic_string('abbbaba')
    'abbba'
    >>> palindromic_string('ababa')
    'ababa'

    Manacher 算法在线性时间内找出最长回文子串。

    1. 先将 input_string("xyx") 转为 new_string("x|y|x")，其中奇数
        位置为实际输入字符。
    2. 对于 new_string 中的每个字符，求出对应长度，
        保存长度，并用 left、right 记录先前计算的信息。
        （详情请参阅说明）

    3. 移除所有 "|"，返回相应的 output_string
    """
    max_length = 0

    # 若 input_string 为 "aba"，则 new_input_string 变为 "a|b|a"
    new_input_string = ""
    output_string = ""

    # 在 range(0, length-1) 范围内，将各字符及 "|" 追加到 new_string
    for i in input_string[: len(input_string) - 1]:
        new_input_string += i + "|"
    # 追加最后一个字符
    new_input_string += input_string[-1]

    # 保存此前右端延伸最远的回文
    # 子串的起止位置
    left, right = 0, 0

    # length[i] 表示以 i 为中心的回文子串长度
    length = [1 for i in range(len(new_input_string))]

    # 为 new_string 中的每个字符寻找对应的回文串
    start = 0
    for j in range(len(new_input_string)):
        k = 1 if j > right else min(length[left + right - j] // 2, right - j + 1)
        while (
            j - k >= 0
            and j + k < len(new_input_string)
            and new_input_string[k + j] == new_input_string[j - k]
        ):
            k += 1

        length[j] = 2 * k - 1

        # 此字符串的结束位置是否超过此前探索的右端点 right？
        # 若是，则将 right 更新为该字符串的最后一个索引
        if j + k - 1 > right:
            left = j - k + 1
            right = j + k - 1

        # 更新 max_length 和起始位置
        if max_length < length[j]:
            max_length = length[j]
            start = j

    # 构造该字符串
    s = new_input_string[start - max_length // 2 : start + max_length // 2 + 1]
    for i in s:
        if i != "|":
            output_string += i

    return output_string


if __name__ == "__main__":
    import doctest

    doctest.testmod()

"""
...a0...a1...a2.....a3......a4...a5...a6....

设需要求最长回文子串的字符串如上所示，
其中 ... 表示中间的若干字符。现在要计算
以 a5 为中心的回文子串长度，且满足以下条件：
i) 已保存以 a3 为中心的回文子串长度，
    该子串从 left 开始到 right 结束，是目前右端延伸最远的回文，
    且结束位置在 a6 之后
ii) a2 和 a4 到 a3 的距离相同，因此 char(a2) == char(a4)
iii) a0 和 a6 到 a3 的距离相同，因此 char(a0) == char(a6)
iv) 在以 a3 为中心的回文中，a1 是 a5 对应的相同字符（请在下面
    推导 a4==a6 时记住这一点）

现在计算以 a5 为中心的回文子串长度，
是否可以利用先前计算的信息？
可以。从上图可知，a5 位于以 a3 为中心的回文中，
且此前已得知
a0==a2（以 a1 为中心的回文）
a2==a4（以 a3 为中心的回文）
a0==a6（以 a3 为中心的回文）
因此 a4==a6

所以，以 a5 为中心的回文至少与以 a1 为中心的回文一样长，
但这仅在 a0 和 a6 均位于以 a3 为中心的回文范围内时成立，
最终得到：

len_of_palindrome__at(a5) = min(len_of_palindrome_at(a1), right-a5)
其中以 a3 为中心的回文从 left 延伸到 right，需要不断更新此范围

若 a5 位于 left、right 边界之外，则用暴力法计算回文长度，
并更新 left、right。

与 Z 函数一样，这可实现线性时间复杂度
"""
