"""
假设：
    - 待压缩的值可以相互比较，即可排序并使用 '<' 和 '>' 运算符比较。
"""


class CoordinateCompressor:
    """
    用于坐标压缩的类。

    此类可对值列表进行压缩和解压缩。

    映射：
    除压缩和解压缩外，此类还使用字典 `coordinate_map` 和列表 `reverse_map`
    维护原始值与压缩值之间的映射：
    - `coordinate_map`：将原始值映射到压缩坐标的字典，键为原始值，值为压缩坐标。
    - `reverse_map`：用于反向映射的列表，每个索引对应一个压缩坐标，
      该索引处的值为原始值。

    映射示例：
    原始值：10，压缩值：0
    原始值：52，压缩值：1
    原始值：83，压缩值：2
    原始值：100，压缩值：3

    此映射可以高效压缩和解压缩列表中的值。
    """

    def __init__(self, arr: list[int | float | str]) -> None:
        """
        使用列表初始化 CoordinateCompressor。

        参数：
        arr: 待压缩的值列表。

        >>> arr = [100, 10, 52, 83]
        >>> cc = CoordinateCompressor(arr)
        >>> cc.compress(100)
        3
        >>> cc.compress(52)
        1
        >>> cc.decompress(1)
        52
        """

        # 存储压缩坐标的字典
        self.coordinate_map: dict[int | float | str, int] = {}

        # 存储反向映射的列表
        self.reverse_map: list[int | float | str] = [-1] * len(arr)

        self.arr = sorted(arr)  # 输入列表
        self.n = len(arr)  # 输入列表的长度
        self.compress_coordinates()

    def compress_coordinates(self) -> None:
        """
        压缩输入列表中的坐标。

        >>> arr = [100, 10, 52, 83]
        >>> cc = CoordinateCompressor(arr)
        >>> cc.coordinate_map[83]
        2
        >>> cc.coordinate_map[80]  # Value not in the original list
        Traceback (most recent call last):
            ...
        KeyError: 80
        >>> cc.reverse_map[2]
        83
        """
        key = 0
        for val in self.arr:
            if val not in self.coordinate_map:
                self.coordinate_map[val] = key
                self.reverse_map[key] = val
                key += 1

    def compress(self, original: float | str) -> int:
        """
        压缩单个值。

        参数：
        original: 待压缩的值。

        返回：
        压缩后的整数。

        异常：
        KeyError: ``original`` 不在输入列表中时引发。

        >>> arr = [100, 10, 52, 83]
        >>> cc = CoordinateCompressor(arr)
        >>> cc.compress(100)
        3
        >>> cc.compress(7)  # Value not in the original list
        Traceback (most recent call last):
            ...
        KeyError: 7
        """
        return self.coordinate_map[original]

    def decompress(self, num: int) -> int | float | str:
        """
        解压缩单个整数。

        参数：
        num: 待解压缩的压缩整数。

        返回：
        原始值。

        异常：
        IndexError: ``num`` 不是有效压缩坐标时引发。

        >>> arr = [100, 10, 52, 83]
        >>> cc = CoordinateCompressor(arr)
        >>> cc.decompress(0)
        10
        >>> cc.decompress(5)  # Compressed coordinate out of range
        Traceback (most recent call last):
            ...
        IndexError: compressed coordinate 5 is out of range
        """
        if not 0 <= num < len(self.reverse_map):
            msg = f"compressed coordinate {num} is out of range"
            raise IndexError(msg)
        return self.reverse_map[num]


if __name__ == "__main__":
    from doctest import testmod

    testmod()

    arr: list[int | float | str] = [100, 10, 52, 83]
    cc = CoordinateCompressor(arr)

    for original in arr:
        compressed = cc.compress(original)
        decompressed = cc.decompress(compressed)
        print(f"Original: {decompressed}, Compressed: {compressed}")
