#!/usr/bin/env python3
from abc import abstractmethod

from .number_theory.prime_numbers import next_prime


class HashTable:
    """
    Basic 哈希表 示例 带有 开放 寻址 并且 linear probing
    """

    def __init__(
        self,
        size_table: int,
        charge_factor: int | None = None,
        lim_charge: float | None = None,
    ) -> None:
        self.size_table = size_table
        self.values = [None] * self.size_table
        self.lim_charge = 0.75 if lim_charge is None else lim_charge
        self.charge_factor = 1 if charge_factor is None else charge_factor
        self.__aux_list: list = []
        self._keys: dict = {}

    def keys(self) -> dict:
        """
        键 函数 返回值 dictionary 包含 该键 值 对。
        键 being 该索引 数 在 哈希表 并且 值 being 数据 值。

        示例：
        1. creating HashTable 带有 大小 10 并且 inserting 3 元素
        >>> ht = HashTable(10)
        >>> ht.insert_data(10)
        >>> ht.insert_data(20)
        >>> ht.insert_data(30)
        >>> ht.keys()
        {0: 10, 1: 20, 2: 30}

        2. creating HashTable 带有 大小 5 并且 inserting 5 元素
        >>> ht = HashTable(5)
        >>> ht.insert_data(5)
        >>> ht.insert_data(4)
        >>> ht.insert_data(3)
        >>> ht.insert_data(2)
        >>> ht.insert_data(1)
        >>> ht.keys()
        {0: 5, 4: 4, 3: 3, 2: 2, 1: 1}
        """
        return self._keys

    def balanced_factor(self) -> float:
        return sum(1 for slot in self.values if slot is not None) / (
            self.size_table * self.charge_factor
        )

    def hash_function(self, key) -> int:
        """
        Generates 哈希 用于 给定 键 值

        示例：

        Creating HashTable 带有 大小 5
        >>> ht = HashTable(5)
        >>> ht.hash_function(10)
        0
        >>> ht.hash_function(20)
        0
        >>> ht.hash_function(4)
        4
        >>> ht.hash_function(18)
        3
        >>> ht.hash_function(-18)
        2
        >>> ht.hash_function(18.5)
        3.5
        >>> ht.hash_function(0)
        0
        >>> ht.hash_function(-0)
        0
        """
        return key % self.size_table

    def _step_by_step(self, step_ord) -> None:
        print(f"step {step_ord}")
        print(list(range(len(self.values))))
        print(self.values)

    def bulk_insert(self, values) -> None:
        """
        bulk_insert 是 使用 用于 entering 更多 比 一个 元素 在 时间
        在 HashTable。

        示例：
        1.
        >>> ht = HashTable(5)
        >>> ht.bulk_insert((10,20,30))
        step 1
        [0, 1, 2, 3, 4]
        [10, None, None, None, None]
        step 2
        [0, 1, 2, 3, 4]
        [10, 20, None, None, None]
        step 3
        [0, 1, 2, 3, 4]
        [10, 20, 30, None, None]

        2.
        >>> ht = HashTable(5)
        >>> ht.bulk_insert([5,4,3,2,1])
        step 1
        [0, 1, 2, 3, 4]
        [5, None, None, None, None]
        step 2
        [0, 1, 2, 3, 4]
        [5, None, None, None, 4]
        step 3
        [0, 1, 2, 3, 4]
        [5, None, None, 3, 4]
        step 4
        [0, 1, 2, 3, 4]
        [5, None, 2, 3, 4]
        step 5
        [0, 1, 2, 3, 4]
        [5, 1, 2, 3, 4]
        """
        i = 1
        self.__aux_list = values
        for value in values:
            self.insert_data(value)
            self._step_by_step(i)
            i += 1

    def _set_value(self, key, data) -> None:
        """
        _set_value 函数 允许 到 更新 值 在 particular 哈希

        示例：
        1. _set_value 在 HashTable 的 大小 5
        >>> ht = HashTable(5)
        >>> ht.insert_data(10)
        >>> ht.insert_data(20)
        >>> ht.insert_data(30)
        >>> ht._set_value(0,15)
        >>> ht.keys()
        {0: 15, 1: 20, 2: 30}

        2. _set_value 在 HashTable 的 大小 2
        >>> ht = HashTable(2)
        >>> ht.insert_data(17)
        >>> ht.insert_data(18)
        >>> ht.insert_data(99)
        >>> ht._set_value(3,15)
        >>> ht.keys()
        {3: 15, 2: 17, 4: 99}

        3. _set_value 在 HashTable 当 哈希 是 不 存在
        >>> ht = HashTable(2)
        >>> ht.insert_data(17)
        >>> ht.insert_data(18)
        >>> ht.insert_data(99)
        >>> ht._set_value(0,15)
        >>> ht.keys()
        {3: 18, 2: 17, 4: 99, 0: 15}

        4. _set_value 在 HashTable 当 multiple 哈希 是 不 存在
        >>> ht = HashTable(2)
        >>> ht.insert_data(17)
        >>> ht.insert_data(18)
        >>> ht.insert_data(99)
        >>> ht._set_value(0,15)
        >>> ht._set_value(1,20)
        >>> ht.keys()
        {3: 18, 2: 17, 4: 99, 0: 15, 1: 20}
        """
        self.values[key] = data
        self._keys[key] = data

    @abstractmethod
    def _collision_resolution(self, key, data=None):
        """
        此方法 是 类型 的 开放 寻址 其 是 使用 用于 handling collision。

        在 此 实现 concept 的 linear probing 具有 been 使用。

        哈希表 是 已搜索 sequentially 从 原始 location 的
        哈希，如果 新 哈希/location 我们 获取 是 已经 occupied 我们 检查 用于 下一个
        哈希/location。

        引用：
            - https://en.wikipedia.org/wiki/Linear_probing

        示例：
        1. collision 将 为 带有 键 18 & 99，因此 新 哈希 将 为 created 用于 99
        >>> ht = HashTable(3)
        >>> ht.insert_data(17)
        >>> ht.insert_data(18)
        >>> ht.insert_data(99)
        >>> ht.keys()
        {2: 17, 0: 18, 1: 99}

        2. collision 将 为 带有 键 17 & 101，因此 新 哈希
        将 为 created 用于 101
        >>> ht = HashTable(4)
        >>> ht.insert_data(17)
        >>> ht.insert_data(18)
        >>> ht.insert_data(99)
        >>> ht.insert_data(101)
        >>> ht.keys()
        {1: 17, 2: 18, 3: 99, 0: 101}

        2. collision 将 为 带有 所有 键，因此 新 哈希 将 为 created 用于 所有
        >>> ht = HashTable(1)
        >>> ht.insert_data(17)
        >>> ht.insert_data(18)
        >>> ht.insert_data(99)
        >>> ht.keys()
        {2: 17, 3: 18, 4: 99}

        3. Trying 到 插入 浮点数 键 在 哈希
        >>> ht = HashTable(1)
        >>> ht.insert_data(17)
        >>> ht.insert_data(18)
        >>> ht.insert_data(99.99)
        Traceback (most recent call last):
        ...
        TypeError: list indices must be integers or slices, not float
        """
        new_key = self.hash_function(key + 1)

        while self.values[new_key] is not None and self.values[new_key] != key:
            if self.values.count(None) > 0:
                new_key = self.hash_function(new_key + 1)
            else:
                new_key = None
                break

        return new_key

    def rehashing(self) -> None:
        survivor_values = [value for value in self.values if value is not None]
        self.size_table = next_prime(self.size_table, factor=2)
        self._keys.clear()
        self.values = [None] * self.size_table  # hell's 指针 D: don't DRY ;/
        for value in survivor_values:
            self.insert_data(value)

    def insert_data(self, data) -> None:
        """
        insert_data 是 使用 用于 inserting 单个元素 在 时间 在 HashTable。

        示例：

        >>> ht = HashTable(3)
        >>> ht.insert_data(5)
        >>> ht.keys()
        {2: 5}
        >>> ht = HashTable(5)
        >>> ht.insert_data(30)
        >>> ht.insert_data(50)
        >>> ht.keys()
        {0: 30, 1: 50}
        """
        key = self.hash_function(data)

        if self.values[key] is None:
            self._set_value(key, data)

        elif self.values[key] == data:
            pass

        else:
            collision_resolution = self._collision_resolution(key, data)
            if collision_resolution is not None:
                self._set_value(collision_resolution, data)
            else:
                self.rehashing()
                self.insert_data(data)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
