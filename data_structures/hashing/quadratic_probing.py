#!/usr/bin/env python3

from .hash_table import HashTable


class QuadraticProbing(HashTable):
    """
    Basic 哈希表 示例 带有 开放 寻址 使用 Quadratic Probing
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def _collision_resolution(self, key, data=None):  # noqa: ARG002
        """
        Quadratic probing 是 开放 寻址 scheme 使用 用于 resolving
        collisions 在 哈希表。

        它 works 通过 taking 原始 哈希 索引 并且 添加 successive
        值 的 arbitrary quadratic polynomial until 开放 slot 是 找到。

        哈希 + 1²，哈希 + 2²，哈希 + 3² .... 哈希 + n²

        引用：
            - https://en.wikipedia.org/wiki/Quadratic_probing
        e.g:
        1. 创建 哈希表 带有 大小 7
        >>> qp = QuadraticProbing(7)
        >>> qp.insert_data(90)
        >>> qp.insert_data(340)
        >>> qp.insert_data(24)
        >>> qp.insert_data(45)
        >>> qp.insert_data(99)
        >>> qp.insert_data(73)
        >>> qp.insert_data(7)
        >>> qp.keys()
        {11: 45, 14: 99, 7: 24, 0: 340, 5: 73, 6: 90, 8: 7}

        2. 创建 哈希表 带有 大小 8
        >>> qp = QuadraticProbing(8)
        >>> qp.insert_data(0)
        >>> qp.insert_data(999)
        >>> qp.insert_data(111)
        >>> qp.keys()
        {0: 0, 7: 999, 3: 111}

        3. Try 到 添加 three 数据 元素 当 大小 是 两个
        >>> qp =  QuadraticProbing(2)
        >>> qp.insert_data(0)
        >>> qp.insert_data(999)
        >>> qp.insert_data(111)
        >>> qp.keys()
        {0: 0, 4: 999, 1: 111}

        4. Try 到 添加 three 数据 元素 当 大小 是 一个
        >>> qp =  QuadraticProbing(1)
        >>> qp.insert_data(0)
        >>> qp.insert_data(999)
        >>> qp.insert_data(111)
        >>> qp.keys()
        {4: 999, 1: 111}
        """

        i = 1
        new_key = self.hash_function(key + i * i)

        while self.values[new_key] is not None and self.values[new_key] != key:
            i += 1
            new_key = (
                self.hash_function(key + i * i)
                if not self.balanced_factor() >= self.lim_charge
                else None
            )

            if new_key is None:
                break

        return new_key


if __name__ == "__main__":
    import doctest

    doctest.testmod()
