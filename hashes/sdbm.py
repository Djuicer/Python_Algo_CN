"""
该算法是为 sdbm 数据库库（ndbm 的公有领域重新实现）创建的。
实践发现，它能很好地扰乱比特，使键的分布更均匀，并减少分裂。
它也是一种分布良好的通用哈希函数。
实际函数（伪代码）如下：
    for i in i..len(str):
        hash(i) = hash(i - 1) * 65599 + str[i];

下面给出的是 gawk 使用的较快版本。[另有使用 Duff 装置的更快版本]
魔数 65599 是在尝试不同常数时凭经验选出的，后来发现它恰好是一个质数。
这是 Berkeley DB（参见 Sleepycat）等软件所采用的算法之一。

来源：http://www.cse.yorku.ca/~oz/hash.html
"""


def sdbm(plain_text: str) -> int:
    """
    实现易于使用且擅长扰乱比特的 sdbm 哈希。
    遍历给定字符串中的每个字符，并逐一应用哈希函数。

    >>> sdbm('Algorithms')
    1462174910723540325254304520539387479031000036

    >>> sdbm('scramble bits')
    730247649148944819640658295400555317318720608290373040936089
    """
    hash_value = 0
    for plain_chr in plain_text:
        hash_value = (
            ord(plain_chr) + (hash_value << 6) + (hash_value << 16) - hash_value
        )
    return hash_value
