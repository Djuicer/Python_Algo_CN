"""
该算法（k=33）最早由 Dan Bernstein 多年前在 comp.lang.c 中提出。
该算法的另一版本（Bernstein 目前更青睐此版本）使用异或：
    hash(i) = hash(i - 1) * 33 ^ str[i];

    第一个魔数 33：
    它为何有效一直没有得到充分解释。
    它的神奇之处在于，无论与质数还是非质数相比，其效果都优于许多其他常数。

    第二个魔数 5381：

    1. 奇数
    2. 质数
    3. 亏数
    4. 001/010/100/000/101 b

    来源：http://www.cse.yorku.ca/~oz/hash.html
"""


def djb2(s: str) -> int:
    """
    实现 djb2 哈希算法；该算法因其魔数而广受欢迎。

    >>> djb2('Algorithms')
    3782405311

    >>> djb2('scramble bits')
    1609059040
    """
    hash_value = 5381
    for x in s:
        hash_value = ((hash_value << 5) + hash_value) + ord(x)
    return hash_value & 0xFFFFFFFF
