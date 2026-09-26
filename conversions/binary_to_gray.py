"""
二进制到格雷码（Gray Code）的转换算法。

参考资料：
https://en.wikipedia.org/wiki/Gray_code
"""


def binary_to_gray(binary: str) -> str:
    """
    将以字符串表示的二进制数转换为等价的格雷码。

    将每一位与其前一位进行异或运算以生成格雷码。

    参数：
        binary (str)：表示二进制数的字符串（例如 "10101010"）。

    返回：
        str：对应的格雷码字符串。

    示例：
        >>> binary_to_gray("10101010")
        '11111111'

        >>> binary_to_gray("1101")
        '1011'
    """
    # 将二进制字符串转换为整数
    binary_int = int(binary, 2)

    # 将二进制数与自身右移 1 位后的结果进行异或
    gray_int = binary_int ^ (binary_int >> 1)

    # 将整数结果转换回二进制字符串（移除 '0b' 前缀）
    gray_code = bin(gray_int)[2:]

    # 在前面补零，使位数与输入相同
    return gray_code.zfill(len(binary))


if __name__ == "__main__":
    # 获取用户输入
    binary_input = input("Enter a binary number: ").strip()

    # 验证输入（只允许 0 和 1）
    if not all(bit in "01" for bit in binary_input):
        print("❌ Invalid input! Please enter only 0s and 1s.")
    else:
        result = binary_to_gray(binary_input)
        print(f"✅ The Gray code for binary {binary_input} is: {result}")
