"""
Lempel-Ziv-Welch 压缩算法的多种实现之一。
https://en.wikipedia.org/wiki/Lempel%E2%80%93Ziv%E2%80%93Welch
"""

import math
import os
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


def add_key_to_lexicon(
    lexicon: dict[str, str], curr_string: str, index: int, last_match_id: str
) -> None:
    """
    将新字符串（curr_string + "0"、curr_string + "1"）添加到词典。
    """
    lexicon.pop(curr_string)
    lexicon[curr_string + "0"] = last_match_id

    if math.log2(index).is_integer():
        for curr_key, value in lexicon.items():
            lexicon[curr_key] = f"0{value}"

    lexicon[curr_string + "1"] = bin(index)[2:]


def compress_data(data_bits: str) -> str:
    """
    使用 Lempel-Ziv-Welch 压缩算法压缩给定的 data_bits，并以字符串返回结果。
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
        add_key_to_lexicon(lexicon, curr_string, index, last_match_id)
        index += 1
        curr_string = ""

    while curr_string != "" and curr_string not in lexicon:
        curr_string += "0"

    if curr_string != "":
        last_match_id = lexicon[curr_string]
        result += last_match_id

    return result


def add_file_length(source_path: str, compressed: str) -> str:
    """
    使用 Elias 伽马编码将给定文件的长度添加到压缩字符串前。
    """
    file_length = os.path.getsize(source_path)
    file_length_binary = bin(file_length)[2:]
    length_length = len(file_length_binary)

    return "0" * (length_length - 1) + file_length_binary + compressed


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

            for elem in result_byte_array:
                opened_file.write(int(elem, 2).to_bytes(1, byteorder="big"))
    except OSError:
        print("File not accessible")
        sys.exit()


def compress(source_path: str, destination_path: str) -> None:
    """
    读取源文件，将其压缩，并把压缩结果写入目标文件。
    """
    data_bits = read_file_binary(source_path)
    compressed = compress_data(data_bits)
    compressed = add_file_length(source_path, compressed)
    write_file_binary(destination_path, compressed)


if __name__ == "__main__":
    compress(sys.argv[1], sys.argv[2])
