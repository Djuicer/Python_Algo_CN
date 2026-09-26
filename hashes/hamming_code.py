# Author: João Gustavo A. Amorim & Gabriel Kunz
# Author email: joaogustavoamorim@gmail.com and gabriel-kunz@uergs.edu.br
# Coding date:  apr 2019
# Black: True

"""
* 本代码实现汉明码（Hamming Code）：
    https://en.wikipedia.org/wiki/Hamming_code —— 在电信领域，汉明码是一类
线性纠错码。汉明码能够检测最多两个比特的错误，或纠正一个比特的错误，
但无法检测未纠正的错误。相比之下，简单奇偶校验码无法纠正错误，并且只能
检测奇数个比特的错误。汉明码是完备码，即在给定分组长度且最小距离为 3 时，
它能达到可能的最高码率。

* 实现的代码包括：
    * 负责对消息编码的函数（emitterConverter）
        * 返回编码后的消息
    * 负责对消息解码的函数（receptorConverter）
        * 返回解码后的消息及数据完整性确认

* 使用方法：
        使用时必须声明要在消息中加入多少个奇偶校验位（sizePari）。
        出于测试目的，可以选择一个比特并将其设为错误值，以检查代码是否
    正常工作。
        最后，指定要编码的消息或单词变量（text）。

* 工作原理：
        声明变量（sizePari、be、text）

        使用 text_to_bits 函数将消息或单词（text）转换为二进制
        按照汉明编码规则对消息编码
        按照汉明编码规则对消息解码
        输出原始消息、编码后的消息和解码后的消息

        在编码文本变量中强制引入错误
        对被强制引入错误的消息进行解码
        输出原始消息、编码后的消息、比特已改变的消息和解码后的消息
"""

# 导入依赖
import numpy as np


# 二进制转换函数------------------------------------------------------
def text_to_bits(text, encoding="utf-8", errors="surrogatepass"):
    """
    >>> text_to_bits("msg")
    '011011010111001101100111'
    """
    bits = bin(int.from_bytes(text.encode(encoding, errors), "big"))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))


def text_from_bits(bits, encoding="utf-8", errors="surrogatepass"):
    """
    >>> text_from_bits('011011010111001101100111')
    'msg'
    """
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, "big").decode(encoding, errors) or "\0"


# 汉明码函数-----------------------------------------------------------
def emitter_converter(size_par, data):
    """
    :param size_par: 消息必须包含的奇偶校验位数量
    :param data: 信息位
    :return: 要通过不可靠介质传输的消息
            - 信息位与奇偶校验位合并后的比特序列

    >>> emitter_converter(4, "101010111111")
    ['1', '1', '1', '1', '0', '1', '0', '0', '1', '0', '1', '1', '1', '1', '1', '1']
    >>> emitter_converter(5, "101010111111")
    Traceback (most recent call last):
        ...
    ValueError: size of parity don't match with size of data
    """
    if size_par + len(data) <= 2**size_par - (len(data) - 1):
        raise ValueError("size of parity don't match with size of data")

    data_out = []
    parity = []
    bin_pos = [bin(x)[2:] for x in range(1, size_par + len(data) + 1)]

    # 根据输出数据大小排列信息数据
    data_ord = []
    # 数据位置模板及奇偶校验位
    data_out_gab = []
    # 奇偶校验位计数器
    qtd_bp = 0
    # 数据位位置计数器
    cont_data = 0

    for x in range(1, size_par + len(data) + 1):
        # 构建比特位置模板：哪些位置放数据，哪些位置放奇偶校验位
        if qtd_bp < size_par:
            if (np.log(x) / np.log(2)).is_integer():
                data_out_gab.append("P")
                qtd_bp = qtd_bp + 1
            else:
                data_out_gab.append("D")
        else:
            data_out_gab.append("D")

        # 按新的输出大小排列数据
        if data_out_gab[-1] == "D":
            data_ord.append(data[cont_data])
            cont_data += 1
        else:
            data_ord.append(None)

    # 计算奇偶校验位
    for bp in range(1, size_par + 1):
        # 给定奇偶校验位所覆盖的 1 比特计数器
        cont_bo = 0
        # 控制循环读取的计数器
        for cont_loop, x in enumerate(data_ord):
            if x is not None:
                try:
                    aux = (bin_pos[cont_loop])[-1 * (bp)]
                except IndexError:
                    aux = "0"
                if aux == "1" and x == "1":
                    cont_bo += 1
        parity.append(cont_bo % 2)

    # 组装消息
    cont_bp = 0  # 奇偶校验位计数器
    for x in range(size_par + len(data)):
        if data_ord[x] is None:
            data_out.append(str(parity[cont_bp]))
            cont_bp += 1
        else:
            data_out.append(data_ord[x])

    return data_out


def receptor_converter(size_par, data):
    """
    >>> receptor_converter(4, "1111010010111111")
    (['1', '0', '1', '0', '1', '0', '1', '1', '1', '1', '1', '1'], True)
    """
    # 数据位置模板及奇偶校验位
    data_out_gab = []
    # 奇偶校验位计数器
    qtd_bp = 0
    # 数据位读取计数器
    cont_data = 0
    # 接收到的奇偶校验位列表
    parity_received = []
    data_output = []

    for i, item in enumerate(data, 1):
        # 构建比特位置模板：哪些位置放数据，哪些位置放奇偶校验位
        if qtd_bp < size_par and (np.log(i) / np.log(2)).is_integer():
            data_out_gab.append("P")
            qtd_bp = qtd_bp + 1
        else:
            data_out_gab.append("D")

        # 按新的输出大小排列数据
        if data_out_gab[-1] == "D":
            data_output.append(item)
        else:
            parity_received.append(item)

    # -----------根据数据计算奇偶校验位
    data_out = []
    parity = []
    bin_pos = [bin(x)[2:] for x in range(1, size_par + len(data_output) + 1)]

    # 根据输出数据大小排列信息数据
    data_ord = []
    # 数据位置反馈及奇偶校验位
    data_out_gab = []
    # 奇偶校验位计数器
    qtd_bp = 0
    # 数据位读取计数器
    cont_data = 0

    for x in range(1, size_par + len(data_output) + 1):
        # 构建比特位置模板：哪些位置放数据，哪些位置放奇偶校验位
        if qtd_bp < size_par and (np.log(x) / np.log(2)).is_integer():
            data_out_gab.append("P")
            qtd_bp = qtd_bp + 1
        else:
            data_out_gab.append("D")

        # 按新的输出大小排列数据
        if data_out_gab[-1] == "D":
            data_ord.append(data_output[cont_data])
            cont_data += 1
        else:
            data_ord.append(None)

    # 计算奇偶校验位
    for bp in range(1, size_par + 1):
        # 某个奇偶校验位所覆盖的 1 比特计数器
        cont_bo = 0
        for cont_loop, x in enumerate(data_ord):
            if x is not None:
                try:
                    aux = (bin_pos[cont_loop])[-1 * (bp)]
                except IndexError:
                    aux = "0"
                if aux == "1" and x == "1":
                    cont_bo += 1
        parity.append(str(cont_bo % 2))

    # 组装消息
    cont_bp = 0  # 奇偶校验位计数器
    for x in range(size_par + len(data_output)):
        if data_ord[x] is None:
            data_out.append(str(parity[cont_bp]))
            cont_bp += 1
        else:
            data_out.append(data_ord[x])

    ack = parity_received == parity
    return data_output, ack


# ---------------------------------------------------------------------
"""
# Example how to use

# number of parity bits
sizePari = 4

# location of the bit that will be forced an error
be = 2

# Message/word to be encoded and decoded with hamming
# text = input("Enter the word to be read: ")
text = "Message01"

# Convert the message to binary
binaryText = text_to_bits(text)

# Prints the binary of the string
print("Text input in binary is '" + binaryText + "'")

# total transmitted bits
totalBits = len(binaryText) + sizePari
print("Size of data is " + str(totalBits))

print("\n --Message exchange--")
print("Data to send ------------> " + binaryText)
dataOut = emitterConverter(sizePari, binaryText)
print("Data converted ----------> " + "".join(dataOut))
dataReceiv, ack = receptorConverter(sizePari, dataOut)
print(
    "Data receive ------------> "
    + "".join(dataReceiv)
    + "\t\t -- Data integrity: "
    + str(ack)
)


print("\n --Force error--")
print("Data to send ------------> " + binaryText)
dataOut = emitterConverter(sizePari, binaryText)
print("Data converted ----------> " + "".join(dataOut))

# forces error
dataOut[-be] = "1" * (dataOut[-be] == "0") + "0" * (dataOut[-be] == "1")
print("Data after transmission -> " + "".join(dataOut))
dataReceiv, ack = receptorConverter(sizePari, dataOut)
print(
    "Data receive ------------> "
    + "".join(dataReceiv)
    + "\t\t -- Data integrity: "
    + str(ack)
)
"""
