"""
Project Euler Problem 79: https://projecteuler.net/problem=79

口令推导

网上银行常用的一种安全方法，是要求用户提供口令中的三个随机字符。例如，若口令为
531278，系统可能要求第 2、第 3 和第 5 个字符；预期回答为 317。

文本文件 keylog.txt 包含五十次成功登录尝试。

已知三个字符总是按顺序询问，分析该文件以确定长度未知的最短可能秘密口令。
"""

import itertools
from pathlib import Path


def find_secret_passcode(logins: list[str]) -> int:
    """
    返回长度未知的最短可能秘密口令。

    >>> find_secret_passcode(["135", "259", "235", "189", "690", "168", "120",
    ...     "136", "289", "589", "160", "165", "580", "369", "250", "280"])
    12365890

    >>> find_secret_passcode(["426", "281", "061", "819" "268", "406", "420",
    ...     "428", "209", "689", "019", "421", "469", "261", "681", "201"])
    4206819
    """

    # 按字符拆分每次登录，例如 '319' -> ('3', '1', '9')
    split_logins = [tuple(login) for login in logins]

    unique_chars = {char for login in split_logins for char in login}

    for permutation in itertools.permutations(unique_chars):
        satisfied = True
        for login in logins:
            if not (
                permutation.index(login[0])
                < permutation.index(login[1])
                < permutation.index(login[2])
            ):
                satisfied = False
                break

        if satisfied:
            return int("".join(permutation))

    raise Exception("Unable to find the secret passcode")


def solution(input_file: str = "keylog.txt") -> int:
    """
    返回由文本文件 `input_file` 中成功登录尝试所确定的、长度未知的最短可能秘密口令。

    >>> solution("keylog_test.txt")
    6312980
    """
    logins = Path(__file__).parent.joinpath(input_file).read_text().splitlines()

    return find_secret_passcode(logins)


if __name__ == "__main__":
    print(f"{solution() = }")
