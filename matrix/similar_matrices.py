"""判断两个方阵是否相似。

若存在可逆矩阵 :math:`P`，使得 :math:`P^{-1} A P = B`，则大小相同的两个方阵
:math:`A` 和 :math:`B` 相似。本实现依赖 SymPy 计算两个矩阵的 Jordan 标准形。
当且仅当两个矩阵的 Jordan 标准形在 Jordan 块置换意义下相等时，它们相似。
* https://en.wikipedia.org/wiki/Jordan_matrix
* https://en.wikipedia.org/wiki/Jordan_normal_form

示例
--------
>>> are_similar_matrices([[3, 1], [0, 3]], [[3, 0], [0, 3]])
False
>>> from sympy import Matrix
>>> matrix_a = [[3, 1], [0, 3]]
>>> transform = Matrix([[1, 1], [0, 1]])
>>> matrix_b = (transform.inv() * Matrix(matrix_a) * transform).tolist()
>>> are_similar_matrices(matrix_a, matrix_b)
True
>>> are_similar_matrices(
...     [[1, 2, 0], [0, 1, 0], [0, 0, 3]],
...     [[1, 0, 0], [0, 1, 0], [0, 0, 3]],
... )
False
>>> are_similar_matrices([[1, 2], [0, 1]], [[1, 2, 0], [0, 1, 0]])
Traceback (most recent call last):
    ...
ValueError: both matrices must be square with the same dimensions
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from sympy import Matrix, nsimplify
from sympy.matrices.common import MatrixError

__all__ = ["are_similar_matrices"]


type MatrixLike = Sequence[Sequence[Any]] | Matrix


def _as_square_matrix(matrix: MatrixLike, *, simplify_entries: bool) -> Matrix:
    """验证 ``matrix`` 为方阵后，返回 SymPy 矩阵。

    参数
    ----------
    matrix:
        描述矩阵元素的嵌套序列（或 SymPy 矩阵）。
    simplify_entries:
        为 ``True`` 时，将每个元素传给 :func:`sympy.nsimplify`，从而把 ``0.5``
        和 ``1/2`` 等值视为相同。

    异常
    ------
    TypeError
        ``matrix`` 无法转换为 SymPy 矩阵时抛出。
    ValueError
        ``matrix`` 不是方阵时抛出。
    """

    try:
        sympy_matrix = Matrix(matrix)
    except (TypeError, ValueError) as exc:  # pragma: no cover - defensive
        msg = "matrix input must be a rectangular sequence of numbers"
        raise TypeError(msg) from exc

    if sympy_matrix.rows != sympy_matrix.cols:
        raise ValueError("both matrices must be square with the same dimensions")

    if simplify_entries:
        sympy_matrix = sympy_matrix.applyfunc(nsimplify)

    return sympy_matrix


def _jordan_signature(matrix: Matrix) -> tuple[tuple[Any, tuple[int, ...]], ...]:
    """返回 ``matrix`` 的 Jordan 标准形的可哈希表示。"""

    _, blocks = matrix.jordan_cells()
    summary: dict[Any, list[int]] = {}
    for block in blocks:
        block_matrix = Matrix(block)
        eigenvalue = block_matrix[0, 0]
        summary.setdefault(eigenvalue, []).append(block_matrix.rows)

    return tuple(
        (
            eigenvalue,
            tuple(sorted(block_sizes, reverse=True)),
        )
        for eigenvalue, block_sizes in sorted(
            summary.items(), key=lambda item: repr(item[0])
        )
    )


def are_similar_matrices(
    matrix_a: MatrixLike,
    matrix_b: MatrixLike,
    *,
    simplify_entries: bool = True,
) -> bool:
    """若 ``matrix_a`` 和 ``matrix_b`` 为相似矩阵，则返回 ``True``。

    参数
    ----------
    matrix_a, matrix_b:
        以嵌套序列（或 SymPy 矩阵）表示的方阵。
    simplify_entries:
        为 ``True``（默认）时，函数会尝试化简每个元素，使代数上相等的值得到
        相同处理。处理应保持不变的符号输入时，可设为 ``False`` 以跳过化简。

    异常
    ------
    ValueError
        矩阵不是方阵或维数不匹配时抛出。
    TypeError
        任一矩阵无法解释为数值矩阵时抛出。
    """

    sympy_a = _as_square_matrix(matrix_a, simplify_entries=simplify_entries)
    sympy_b = _as_square_matrix(matrix_b, simplify_entries=simplify_entries)

    if sympy_a.shape != sympy_b.shape:
        raise ValueError("both matrices must be square with the same dimensions")

    try:
        signature_a = _jordan_signature(sympy_a)
        signature_b = _jordan_signature(sympy_b)
    except MatrixError as exc:  # pragma: no cover - rare SymPy failure
        msg = "unable to determine the Jordan canonical form"
        raise ValueError(msg) from exc

    return signature_a == signature_b


if __name__ == "__main__":  # pragma: no cover - convenience execution
    from doctest import testmod

    testmod()
