"""
Lempel-Ziv-Welch 解压缩算法的多种实现之一。
https://en.wikipedia.org/wiki/Lempel%E2%80%93Ziv%E2%80%93Welch
"""

import math
import sys


def read_file_binary(file_path: str) -> str:
    """
    以字节形式读取给定文件，并将其作为长字符串返回。
    """
    result = ""
    try:
        with open(file_path, "rb") as binary_file:
            data = binary_file.read()
        for dat in data:
            curr_byte = f"{dat:08b}"
            result += curr_byte
        return result
    except OSError:
        print("File not accessible")
        sys.exit()


def decompress_data(data_bits: str) -> str:
    """
    使用 Lempel-Ziv-Welch 算法解压缩给定的 data_bits，并以字符串返回结果。
    """
    lexicon = {"0": "0", "1": "1"}
    result, curr_string = "", ""
    index = len(lexicon)

    for i in range(len(data_bits)):
        curr_string += data_bits[i]
        if curr_string not in lexicon:
            continue

        last_match_id = lexicon[curr_string]
        result += last_match_id
        lexicon[curr_string] = last_match_id + "0"

        if math.log2(index).is_integer():
            new_lex = {}
            for curr_key in list(lexicon):
                new_lex["0" + curr_key] = lexicon.pop(curr_key)
            lexicon = new_lex

        lexicon[bin(index)[2:]] = last_match_id + "1"
        index += 1
        curr_string = ""
    return result


def write_file_binary(file_path: str, to_write: str) -> None:
    """
    将给定的 to_write 字符串（应仅由 0 和 1 组成）以字节形式写入文件。
    """
    byte_length = 8
    try:
        with open(file_path, "wb") as opened_file:
            result_byte_array = [
                to_write[i : i + byte_length]
                for i in range(0, len(to_write), byte_length)
            ]

            if len(result_byte_array[-1]) % byte_length == 0:
                result_byte_array.append("10000000")
            else:
                result_byte_array[-1] += "1" + "0" * (
                    byte_length - len(result_byte_array[-1]) - 1
                )

            for elem in result_byte_array[:-1]:
                opened_file.write(int(elem, 2).to_bytes(1, byteorder="big"))
    except OSError:
        print("File not accessible")
        sys.exit()


def remove_prefix(data_bits: str) -> str:
    """
    移除压缩文件应包含的大小前缀，并返回结果。
    """
    counter = 0
    for letter in data_bits:
        if letter == "1":
            break
        counter += 1

    data_bits = data_bits[counter:]
    data_bits = data_bits[counter + 1 :]
    return data_bits


def compress(source_path: str, destination_path: str) -> None:
    """
    读取源文件，将其解压缩，并把结果写入目标文件。
    """
    data_bits = read_file_binary(source_path)
    data_bits = remove_prefix(data_bits)
    decompressed = decompress_data(data_bits)
    write_file_binary(destination_path, decompressed)


if __name__ == "__main__":
    compress(sys.argv[1], sys.argv[2])
