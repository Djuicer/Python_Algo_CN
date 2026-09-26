from __future__ import annotations

from typing import Any


class Matrix:
    """
    <class Matrix>
    矩阵结构。
    """

    def __init__(self, row: int, column: int, default_value: float = 0) -> None:
        """
        <method Matrix.__init__>
        使用给定大小和默认值初始化矩阵。
        示例：
        >>> a = Matrix(2, 3, 1)
        >>> a
        Matrix consist of 2 rows and 3 columns
        [1, 1, 1]
        [1, 1, 1]
        """

        self.row, self.column = row, column
        self.array = [[default_value for _ in range(column)] for _ in range(row)]

    def __str__(self) -> str:
        """
        <method Matrix.__str__>
        返回此矩阵的字符串表示。
        """

        # 前缀
        s = f"Matrix consist of {self.row} rows and {self.column} columns\n"

        # 构造字符串标识符
        max_element_length = 0
        for row_vector in self.array:
            for obj in row_vector:
                max_element_length = max(max_element_length, len(str(obj)))
        string_format_identifier = f"%{max_element_length}s"

        # 构造并返回字符串
        def single_line(row_vector: list[float]) -> str:
            nonlocal string_format_identifier
            line = "["
            line += ", ".join(string_format_identifier % (obj,) for obj in row_vector)
            line += "]"
            return line

        s += "\n".join(single_line(row_vector) for row_vector in self.array)
        return s

    def __repr__(self) -> str:
        return str(self)

    def validate_indices(self, loc: tuple[int, int]) -> bool:
        """
        <method Matrix.validate_indicies>
        检查给定索引是否可用于从矩阵中选取元素。
        示例：
        >>> a = Matrix(2, 6, 0)
        >>> a.validate_indices((2, 7))
        False
        >>> a.validate_indices((0, 0))
        True
        """
        if not (isinstance(loc, (list, tuple)) and len(loc) == 2):  # noqa: SIM114
            return False
        elif not (0 <= loc[0] < self.row and 0 <= loc[1] < self.column):
            return False
        else:
            return True

    def __getitem__(self, loc: tuple[int, int]) -> Any:
        """
        <method Matrix.__getitem__>
        当 loc = (row, column) 时，返回 array[row][column]。
        示例：
        >>> a = Matrix(3, 2, 7)
        >>> a[1, 0]
        7
        """
        assert self.validate_indices(loc)
        return self.array[loc[0]][loc[1]]

    def __setitem__(self, loc: tuple[int, int], value: float) -> None:
        """
        <method Matrix.__setitem__>
        当 loc = (row, column) 时，设置 array[row][column] = value。
        示例：
        >>> a = Matrix(2, 3, 1)
        >>> a[1, 2] = 51
        >>> a
        Matrix consist of 2 rows and 3 columns
        [ 1,  1,  1]
        [ 1,  1, 51]
        """
        assert self.validate_indices(loc)
        self.array[loc[0]][loc[1]] = value

    def __add__(self, another: Matrix) -> Matrix:
        """
        <method Matrix.__add__>
        返回 self + another。
        示例：
        >>> a = Matrix(2, 1, -4)
        >>> b = Matrix(2, 1, 3)
        >>> a+b
        Matrix consist of 2 rows and 1 columns
        [-1]
        [-1]
        """

        # 验证
        assert isinstance(another, Matrix)
        assert self.row == another.row
        assert self.column == another.column

        # 相加
        result = Matrix(self.row, self.column)
        for r in range(self.row):
            for c in range(self.column):
                result[r, c] = self[r, c] + another[r, c]
        return result

    def __neg__(self) -> Matrix:
        """
        <method Matrix.__neg__>
        返回 -self。
        示例：
        >>> a = Matrix(2, 2, 3)
        >>> a[0, 1] = a[1, 0] = -2
        >>> -a
        Matrix consist of 2 rows and 2 columns
        [-3,  2]
        [ 2, -3]
        """

        result = Matrix(self.row, self.column)
        for r in range(self.row):
            for c in range(self.column):
                result[r, c] = -self[r, c]
        return result

    def __sub__(self, another: Matrix) -> Matrix:
        return self + (-another)

    def __mul__(self, another: float | Matrix) -> Matrix:
        """
        <method Matrix.__mul__>
        返回 self * another。
        示例：
        >>> a = Matrix(2, 3, 1)
        >>> a[0,2] = a[1,2] = 3
        >>> a * -2
        Matrix consist of 2 rows and 3 columns
        [-2, -2, -6]
        [-2, -2, -6]
        """

        if isinstance(another, (int, float)):  # 标量乘法
            result = Matrix(self.row, self.column)
            for r in range(self.row):
                for c in range(self.column):
                    result[r, c] = self[r, c] * another
            return result
        elif isinstance(another, Matrix):  # 矩阵乘法
            assert self.column == another.row
            result = Matrix(self.row, another.column)
            for r in range(self.row):
                for c in range(another.column):
                    for i in range(self.column):
                        result[r, c] += self[r, i] * another[i, c]
            return result
        else:
            msg = f"Unsupported type given for another ({type(another)})"
            raise TypeError(msg)

    def transpose(self) -> Matrix:
        """
        <method Matrix.transpose>
        返回 self^T。
        示例：
        >>> a = Matrix(2, 3)
        >>> for r in range(2):
        ...     for c in range(3):
        ...             a[r,c] = r*c
        ...
        >>> a.transpose()
        Matrix consist of 3 rows and 2 columns
        [0, 0]
        [0, 1]
        [0, 2]
        """

        result = Matrix(self.column, self.row)
        for r in range(self.row):
            for c in range(self.column):
                result[c, r] = self[r, c]
        return result

    def sherman_morrison(self, u: Matrix, v: Matrix) -> Any:
        """
        <method Matrix.sherman_morrison>
        以 O(n^2) 的复杂度应用 Sherman-Morrison 公式。
        该公式参见：
        https://en.wikipedia.org/wiki/Sherman%E2%80%93Morrison_formula
        本方法返回 (A + uv^T)^(-1)，其中 A^(-1) 为 self；若无法计算则返回 None。
        警告：本方法不检查 self 是否可逆，请在执行前确保 self 可逆。
        示例：
        >>> ainv = Matrix(3, 3, 0)
        >>> for i in range(3): ainv[i,i] = 1
        ...
        >>> u = Matrix(3, 1, 0)
        >>> u[0,0], u[1,0], u[2,0] = 1, 2, -3
        >>> v = Matrix(3, 1, 0)
        >>> v[0,0], v[1,0], v[2,0] = 4, -2, 5
        >>> ainv.sherman_morrison(u, v)
        Matrix consist of 3 rows and 3 columns
        [  1.2857142857142856, -0.14285714285714285,   0.3571428571428571]
        [  0.5714285714285714,   0.7142857142857143,   0.7142857142857142]
        [ -0.8571428571428571,  0.42857142857142855,  -0.0714285714285714]
        """

        # 大小验证
        assert isinstance(u, Matrix)
        assert isinstance(v, Matrix)
        assert self.row == self.column == u.row == v.row  # u、v 应为列向量
        assert u.column == v.column == 1  # u、v 应为列向量

        # 计算
        v_t = v.transpose()
        numerator_factor = (v_t * self * u)[0, 0] + 1
        if numerator_factor == 0:
            return None  # 不可逆
        return self - ((self * u) * (v_t * self) * (1.0 / numerator_factor))


# 测试
if __name__ == "__main__":

    def test1() -> None:
        # a^(-1)
        ainv = Matrix(3, 3, 0)
        for i in range(3):
            ainv[i, i] = 1
        print(f"a^(-1) is {ainv}")
        # u, v
        u = Matrix(3, 1, 0)
        u[0, 0], u[1, 0], u[2, 0] = 1, 2, -3
        v = Matrix(3, 1, 0)
        v[0, 0], v[1, 0], v[2, 0] = 4, -2, 5
        print(f"u is {u}")
        print(f"v is {v}")
        print(f"uv^T is {u * v.transpose()}")
        # Sherman Morrison
        print(f"(a + uv^T)^(-1) is {ainv.sherman_morrison(u, v)}")

    def test2() -> None:
        import doctest

        doctest.testmod()

    test2()
