"""
创建于 Mon Feb 26 14:29:11 2018

@author: Christian Bender
@license: MIT-license

本模块包含一些用于在 Python 中处理线性代数的实用类和函数。

概览：

- class Vector
- function zero_vector(dimension)
- function unit_basis_vector(dimension, pos)
- function axpy(scalar, vector1, vector2)
- function random_vector(N, a, b)
- class Matrix
- function square_zero_matrix(N)
- function random_matrix(W, H, a, b)
"""

from __future__ import annotations

import math
import random
from collections.abc import Collection
from typing import overload


class Vector:
    """
    本类表示任意大小的向量，使用时需要给出向量分量。

    方法概览：

        __init__(components: Collection[float] | None): 初始化向量
        __len__(): 获取向量大小（分量数）
        __str__(): 返回字符串表示
        __add__(other: Vector): 向量加法
        __sub__(other: Vector): 向量减法
        __mul__(other: float): 标量乘法
        __mul__(other: Vector): 点积
        copy(): 复制并返回此向量
        component(i): 获取第 i 个分量（从 0 开始索引）
        change_component(pos: int, value: float): 更改指定分量
        euclidean_length(): 返回向量的欧几里得长度
        angle(other: Vector, deg: bool): 返回两个向量的夹角
    """

    def __init__(self, components: Collection[float] | None = None) -> None:
        """
        输入：components 或不传入参数
        用于初始化向量的简单构造函数
        """
        if components is None:
            components = []
        self.__components = list(components)

    def __len__(self) -> int:
        """
        返回向量的大小。
        """
        return len(self.__components)

    def __str__(self) -> str:
        """
        返回向量的字符串表示。
        """
        return "(" + ",".join(map(str, self.__components)) + ")"

    def __add__(self, other: Vector) -> Vector:
        """
        输入：另一个向量
        假设：另一个向量大小相同
        返回表示两者之和的新向量。
        """
        size = len(self)
        if size == len(other):
            result = [self.__components[i] + other.component(i) for i in range(size)]
            return Vector(result)
        else:
            raise Exception("must have the same size")

    def __sub__(self, other: Vector) -> Vector:
        """
        输入：另一个向量
        假设：另一个向量大小相同
        返回表示两者之差的新向量。
        """
        size = len(self)
        if size == len(other):
            result = [self.__components[i] - other.component(i) for i in range(size)]
            return Vector(result)
        else:  # 错误情况
            raise Exception("must have the same size")

    def __eq__(self, other: object) -> bool:
        """
        比较两个向量。
        """
        if not isinstance(other, Vector):
            return NotImplemented
        if len(self) != len(other):
            return False
        return all(self.component(i) == other.component(i) for i in range(len(self)))

    @overload
    def __mul__(self, other: float) -> Vector: ...

    @overload
    def __mul__(self, other: Vector) -> float: ...

    def __mul__(self, other: float | Vector) -> float | Vector:
        """
        mul 实现标量乘法和点积。
        """
        if isinstance(other, (float, int)):
            ans = [c * other for c in self.__components]
            return Vector(ans)
        elif isinstance(other, Vector) and len(self) == len(other):
            size = len(self)
            prods = [self.__components[i] * other.component(i) for i in range(size)]
            return sum(prods)
        else:  # 错误情况
            raise Exception("invalid operand!")

    def copy(self) -> Vector:
        """
        复制并返回此向量。
        """
        return Vector(self.__components)

    def component(self, i: int) -> float:
        """
        输入：索引（从 0 开始）
        输出：向量的第 i 个分量。
        """
        if isinstance(i, int) and -len(self.__components) <= i < len(self.__components):
            return self.__components[i]
        else:
            raise Exception("index out of range")

    def change_component(self, pos: int, value: float) -> None:
        """
        输入：索引（pos）和值
        将指定分量（pos）更改为 'value'。
        """
        # 前置条件
        assert -len(self.__components) <= pos < len(self.__components)
        self.__components[pos] = value

    def euclidean_length(self) -> float:
        """
        返回向量的欧几里得长度。

        >>> Vector([2, 3, 4]).euclidean_length()
        5.385164807134504
        >>> Vector([1]).euclidean_length()
        1.0
        >>> Vector([0, -1, -2, -3, 4, 5, 6]).euclidean_length()
        9.539392014169456
        >>> Vector([]).euclidean_length()
        Traceback (most recent call last):
            ...
        Exception: Vector is empty
        """
        if len(self.__components) == 0:
            raise Exception("Vector is empty")
        squares = [c**2 for c in self.__components]
        return math.sqrt(sum(squares))

    def angle(self, other: Vector, deg: bool = False) -> float:
        """
        求两个向量（self、Vector）之间的夹角。

        >>> Vector([3, 4, -1]).angle(Vector([2, -1, 1]))
        1.4906464636572374
        >>> Vector([3, 4, -1]).angle(Vector([2, -1, 1]), deg = True)
        85.40775111366095
        >>> Vector([3, 4, -1]).angle(Vector([2, -1]))
        Traceback (most recent call last):
            ...
        Exception: invalid operand!
        """
        num = self * other
        den = self.euclidean_length() * other.euclidean_length()
        if deg:
            return math.degrees(math.acos(num / den))
        else:
            return math.acos(num / den)


def zero_vector(dimension: int) -> Vector:
    """
    返回大小为 'dimension' 的零向量。
    """
    # 前置条件
    assert isinstance(dimension, int)
    return Vector([0] * dimension)


def unit_basis_vector(dimension: int, pos: int) -> Vector:
    """
    返回单位基向量，其索引 'pos' 处为 1（索引从 0 开始）。
    """
    # 前置条件
    assert isinstance(dimension, int)
    assert isinstance(pos, int)
    ans = [0] * dimension
    ans[pos] = 1
    return Vector(ans)


def axpy(scalar: float, x: Vector, y: Vector) -> Vector:
    """
    输入：一个 'scalar' 以及两个向量 'x' 和 'y'
    输出：一个向量
    计算 axpy 运算。
    """
    # 前置条件
    assert isinstance(x, Vector)
    assert isinstance(y, Vector)
    assert isinstance(scalar, (int, float))
    return x * scalar + y


def random_vector(n: int, a: int, b: int) -> Vector:
    """
    输入：向量大小（N）和随机范围（a,b）。
    输出：返回大小为 N 的随机向量，其整数分量位于 'a' 和 'b' 之间。
    """
    random.seed(None)
    ans = [random.randint(a, b) for _ in range(n)]
    return Vector(ans)


class Matrix:
    """
    类：Matrix
    本类表示任意矩阵。

    方法概览：

        __init__():
        __str__(): 返回字符串表示
        __add__(other: Matrix): 矩阵加法
        __sub__(other: Matrix): 矩阵减法
        __mul__(other: float): 标量乘法
        __mul__(other: Vector): 向量乘法
        height() : 返回高度
        width() : 返回宽度
        component(x: int, y: int): 返回指定分量
        change_component(x: int, y: int, value: float): 更改指定分量
        minor(x: int, y: int): 返回 (x, y) 处的余子式
        cofactor(x: int, y: int): 返回 (x, y) 处的代数余子式
        determinant() : 返回行列式
    """

    def __init__(self, matrix: list[list[float]], w: int, h: int) -> None:
        """
        使用分量初始化矩阵的简单构造函数。
        """
        self.__matrix = matrix
        self.__width = w
        self.__height = h

    def __str__(self) -> str:
        """
        返回此矩阵的字符串表示。
        """
        ans = ""
        for i in range(self.__height):
            ans += "|"
            for j in range(self.__width):
                if j < self.__width - 1:
                    ans += str(self.__matrix[i][j]) + ","
                else:
                    ans += str(self.__matrix[i][j]) + "|\n"
        return ans

    def __add__(self, other: Matrix) -> Matrix:
        """
        实现矩阵加法。
        """
        if self.__width == other.width() and self.__height == other.height():
            matrix = []
            for i in range(self.__height):
                row = [
                    self.__matrix[i][j] + other.component(i, j)
                    for j in range(self.__width)
                ]
                matrix.append(row)
            return Matrix(matrix, self.__width, self.__height)
        else:
            raise Exception("matrix must have the same dimension!")

    def __sub__(self, other: Matrix) -> Matrix:
        """
        实现矩阵减法。
        """
        if self.__width == other.width() and self.__height == other.height():
            matrix = []
            for i in range(self.__height):
                row = [
                    self.__matrix[i][j] - other.component(i, j)
                    for j in range(self.__width)
                ]
                matrix.append(row)
            return Matrix(matrix, self.__width, self.__height)
        else:
            raise Exception("matrices must have the same dimension!")

    @overload
    def __mul__(self, other: float) -> Matrix: ...

    @overload
    def __mul__(self, other: Vector) -> Vector: ...

    def __mul__(self, other: float | Vector) -> Vector | Matrix:
        """
        实现矩阵与向量的乘法。
        实现矩阵与标量的乘法。
        """
        if isinstance(other, Vector):  # 矩阵与向量相乘
            if len(other) == self.__width:
                ans = zero_vector(self.__height)
                for i in range(self.__height):
                    prods = [
                        self.__matrix[i][j] * other.component(j)
                        for j in range(self.__width)
                    ]
                    ans.change_component(i, sum(prods))
                return ans
            else:
                raise Exception(
                    "vector must have the same size as the "
                    "number of columns of the matrix!"
                )
        elif isinstance(other, (int, float)):  # 矩阵与标量相乘
            matrix = [
                [self.__matrix[i][j] * other for j in range(self.__width)]
                for i in range(self.__height)
            ]
            return Matrix(matrix, self.__width, self.__height)
        return None

    def height(self) -> int:
        """
        获取高度。
        """
        return self.__height

    def width(self) -> int:
        """
        获取宽度。
        """
        return self.__width

    def component(self, x: int, y: int) -> float:
        """
        返回指定的 (x,y) 分量。
        """
        if 0 <= x < self.__height and 0 <= y < self.__width:
            return self.__matrix[x][y]
        else:
            raise Exception("change_component: indices out of bounds")

    def change_component(self, x: int, y: int, value: float) -> None:
        """
        更改此矩阵的 x-y 分量。
        """
        if 0 <= x < self.__height and 0 <= y < self.__width:
            self.__matrix[x][y] = value
        else:
            raise Exception("change_component: indices out of bounds")

    def minor(self, x: int, y: int) -> float:
        """
        返回 (x, y) 处的余子式。
        """
        if self.__height != self.__width:
            raise Exception("Matrix is not square")
        minor = self.__matrix[:x] + self.__matrix[x + 1 :]
        for i in range(len(minor)):
            minor[i] = minor[i][:y] + minor[i][y + 1 :]
        return Matrix(minor, self.__width - 1, self.__height - 1).determinant()

    def cofactor(self, x: int, y: int) -> float:
        """
        返回 (x, y) 处的代数余子式（带符号的余子式）。
        """
        if self.__height != self.__width:
            raise Exception("Matrix is not square")
        if 0 <= x < self.__height and 0 <= y < self.__width:
            return (-1) ** (x + y) * self.minor(x, y)
        else:
            raise Exception("Indices out of bounds")

    def determinant(self) -> float:
        """
        使用拉普拉斯展开返回 nxn 矩阵的行列式。
        """
        if self.__height != self.__width:
            raise Exception("Matrix is not square")
        if self.__height < 1:
            raise Exception("Matrix has no element")
        if self.__height == 1:
            return self.__matrix[0][0]
        elif self.__height == 2:
            return (
                self.__matrix[0][0] * self.__matrix[1][1]
                - self.__matrix[0][1] * self.__matrix[1][0]
            )
        else:
            cofactor_prods = [
                self.__matrix[0][y] * self.cofactor(0, y) for y in range(self.__width)
            ]
            return sum(cofactor_prods)


def square_zero_matrix(n: int) -> Matrix:
    """
    返回维数为 NxN 的方形零矩阵。
    """
    ans: list[list[float]] = [[0] * n for _ in range(n)]
    return Matrix(ans, n, n)


def random_matrix(width: int, height: int, a: int, b: int) -> Matrix:
    """
    返回 WxH 随机矩阵，其整数分量位于 'a' 和 'b' 之间。
    """
    random.seed(None)
    matrix: list[list[float]] = [
        [random.randint(a, b) for _ in range(width)] for _ in range(height)
    ]
    return Matrix(matrix, width, height)
