"""
用 Python 实现单纯形算法，用于求解表格形式的线性规划，其中：
- 约束可以是 `>=`、`<=` 和 `=`；
- 每个变量均满足 `x1, x2, ...>= 0`。

关于如何将线性规划转换为单纯形表，以及单纯形算法的执行步骤，请参阅
https://gist.github.com/imengus/f9619a568f7da5bc74eaf20169a24d98 。

参考资料：
https://en.wikipedia.org/wiki/Simplex_algorithm
https://tinyurl.com/simplex4beginners
"""

from typing import Any

import numpy as np


class Tableau:
    """对单纯形表执行运算。

    >>> Tableau(np.array([[-1,-1,0,0,1],[1,3,1,0,4],[3,1,0,1,4]]), 2, 2)
    Traceback (most recent call last):
    ...
    TypeError: Tableau must have type float64

    >>> Tableau(np.array([[-1,-1,0,0,-1],[1,3,1,0,4],[3,1,0,1,4.]]), 2, 2)
    Traceback (most recent call last):
    ...
    ValueError: RHS must be > 0

    >>> Tableau(np.array([[-1,-1,0,0,1],[1,3,1,0,4],[3,1,0,1,4.]]), -2, 2)
    Traceback (most recent call last):
    ...
    ValueError: number of (artificial) variables must be a natural number
    """

    # 防止循环的最大迭代次数
    maxiter = 100

    def __init__(
        self, tableau: np.ndarray, n_vars: int, n_artificial_vars: int
    ) -> None:
        if tableau.dtype != "float64":
            raise TypeError("Tableau must have type float64")

        # 检查右端项是否为负数
        if not (tableau[:, -1] >= 0).all():
            raise ValueError("RHS must be > 0")

        if n_vars < 2 or n_artificial_vars < 0:
            raise ValueError(
                "number of (artificial) variables must be a natural number"
            )

        self.tableau = tableau
        self.n_rows, n_cols = tableau.shape

        # 决策变量 x1、x2、x3……的数量
        self.n_vars, self.n_artificial_vars = n_vars, n_artificial_vars

        # 若存在 >= 或 == 约束（非标准形式）则为 2，否则（标准形式）为 1
        self.n_stages = (self.n_artificial_vars > 0) + 1

        # 为将不等式化为等式而添加的松弛变量数量
        self.n_slack = n_cols - self.n_vars - self.n_artificial_vars - 1

        # 各阶段的目标
        self.objectives = ["max"]

        # 两阶段单纯形法先最小化，再最大化
        if self.n_artificial_vars:
            self.objectives.append("min")

        self.col_titles = self.generate_col_titles()

        # 当前主元所在行和列的索引
        self.row_idx = None
        self.col_idx = None

        # 目标行是否只包含（非）负值？
        self.stop_iter = False

    def generate_col_titles(self) -> list[str]:
        """为指定维数的单纯形表生成列标题。

        >>> Tableau(np.array([[-1,-1,0,0,1],[1,3,1,0,4],[3,1,0,1,4.]]),
        ... 2, 0).generate_col_titles()
        ['x1', 'x2', 's1', 's2', 'RHS']

        >>> Tableau(np.array([[-1,-1,0,0,1],[1,3,1,0,4],[3,1,0,1,4.]]),
        ... 2, 2).generate_col_titles()
        ['x1', 'x2', 'RHS']
        """
        args = (self.n_vars, self.n_slack)

        # 决策变量 | 松弛变量
        string_starts = ["x", "s"]
        titles = []
        for i in range(2):
            for j in range(args[i]):
                titles.append(string_starts[i] + str(j + 1))
        titles.append("RHS")
        return titles

    def find_pivot(self) -> tuple[Any, Any]:
        """查找主元所在的行和列。
        >>> tuple(int(x) for x in Tableau(np.array([[-2,1,0,0,0], [3,1,1,0,6],
        ... [1,2,0,1,7.]]), 2, 0).find_pivot())
        (1, 0)
        """
        objective = self.objectives[-1]

        # 查找目标行中绝对值最大的元素
        sign = (objective == "min") - (objective == "max")
        col_idx = np.argmax(sign * self.tableau[0, :-1])

        # 最大化时所选值必须小于 0，最小化时必须大于 0
        if sign * self.tableau[0, col_idx] <= 0:
            self.stop_iter = True
            return 0, 0

        # 用主元列元素除右端项时，选择商最小的行作为主元行

        # 排除目标行的切片
        s = slice(self.n_stages, self.n_rows)

        # 右端项（RHS）
        dividend = self.tableau[s, -1]

        # 切片范围内的主元列元素
        divisor = self.tableau[s, col_idx]

        # 用 nan 填充的数组
        nans = np.full(self.n_rows - self.n_stages, np.nan)

        # 若主元列元素大于零则返回商，否则返回 nan
        quotients = np.divide(dividend, divisor, out=nans, where=divisor > 0)

        # 在排除 nan 后取最小商的索引；加上 n_stages 以补偿之前排除的目标行
        row_idx = np.nanargmin(quotients) + self.n_stages
        return row_idx, col_idx

    def pivot(self, row_idx: int, col_idx: int) -> np.ndarray:
        """以主元行和主元列交点处的值为主元执行变换。

        >>> Tableau(np.array([[-2,-3,0,0,0],[1,3,1,0,4],[3,1,0,1,4.]]),
        ... 2, 2).pivot(1, 0).tolist()
        ... # doctest: +NORMALIZE_WHITESPACE
        [[0.0, 3.0, 2.0, 0.0, 8.0],
        [1.0, 3.0, 1.0, 0.0, 4.0],
        [0.0, -8.0, -3.0, 1.0, -8.0]]
        """
        # 避免修改原始单纯形表
        piv_row = self.tableau[row_idx].copy()

        piv_val = piv_row[col_idx]

        # 将该元素化为 1
        piv_row *= 1 / piv_val

        # 使主元列对应变量成为基变量，即该列仅此项非零
        for idx, coeff in enumerate(self.tableau[:, col_idx]):
            self.tableau[idx] += -coeff * piv_row
        self.tableau[row_idx] = piv_row
        return self.tableau

    def change_stage(self) -> np.ndarray:
        """通过删除人工变量对应的行和列退出两阶段法的第一阶段；若退出的是
        标准情形，则完成算法。

        >>> Tableau(np.array([
        ... [3, 3, -1, -1, 0, 0, 4],
        ... [2, 1, 0, 0, 0, 0, 0.],
        ... [1, 2, -1, 0, 1, 0, 2],
        ... [2, 1, 0, -1, 0, 1, 2]
        ... ]), 2, 2).change_stage().tolist()
        ... # doctest: +NORMALIZE_WHITESPACE
        [[2.0, 1.0, 0.0, 0.0, 0.0],
        [1.0, 2.0, -1.0, 0.0, 2.0],
        [2.0, 1.0, 0.0, -1.0, 2.0]]
        """
        # 保留原目标行的目标
        self.objectives.pop()

        if not self.objectives:
            return self.tableau

        # 包含人工变量列索引的切片
        s = slice(-self.n_artificial_vars - 1, -1)

        # 删除人工变量列
        self.tableau = np.delete(self.tableau, s, axis=1)

        # 删除第一阶段的目标行
        self.tableau = np.delete(self.tableau, 0, axis=0)

        self.n_stages = 1
        self.n_rows -= 1
        self.n_artificial_vars = 0
        self.stop_iter = False
        return self.tableau

    def run_simplex(self) -> dict[Any, Any]:
        """操作单纯形表，直至目标函数无法继续改进。

        # 标准线性规划：
        Max:  x1 +  x2
        ST:   x1 + 3x2 <= 4
             3x1 +  x2 <= 4
        >>> {key: float(value) for key, value in Tableau(np.array([[-1,-1,0,0,0],
        ... [1,3,1,0,4],[3,1,0,1,4.]]), 2, 0).run_simplex().items()}
        {'P': 2.0, 'x1': 1.0, 'x2': 1.0}

        # 含 3 个变量的标准线性规划：
        Max: 3x1 +  x2 + 3x3
        ST:  2x1 +  x2 +  x3 ≤ 2
              x1 + 2x2 + 3x3 ≤ 5
             2x1 + 2x2 +  x3 ≤ 6
        >>> {key: float(value) for key, value in Tableau(np.array([
        ... [-3,-1,-3,0,0,0,0],
        ... [2,1,1,1,0,0,2],
        ... [1,2,3,0,1,0,5],
        ... [2,2,1,0,0,1,6.]
        ... ]),3,0).run_simplex().items()} # doctest: +ELLIPSIS
        {'P': 5.4, 'x1': 0.199..., 'x3': 1.6}


        # 输入最优单纯形表：
        >>> {key: float(value) for key, value in Tableau(np.array([
        ... [0, 0, 0.25, 0.25, 2],
        ... [0, 1, 0.375, -0.125, 1],
        ... [1, 0, -0.125, 0.375, 1]
        ... ]), 2, 0).run_simplex().items()}
        {'P': 2.0, 'x1': 1.0, 'x2': 1.0}

        # 非标准形式：>= 约束
        Max: 2x1 + 3x2 +  x3
        ST:   x1 +  x2 +  x3 <= 40
             2x1 +  x2 -  x3 >= 10
                 -  x2 +  x3 >= 10
        >>> {key: float(value) for key, value in Tableau(np.array([
        ... [2, 0, 0, 0, -1, -1, 0, 0, 20],
        ... [-2, -3, -1, 0, 0, 0, 0, 0, 0],
        ... [1, 1, 1, 1, 0, 0, 0, 0, 40],
        ... [2, 1, -1, 0, -1, 0, 1, 0, 10],
        ... [0, -1, 1, 0, 0, -1, 0, 1, 10.]
        ... ]), 3, 2).run_simplex().items()}
        {'P': 70.0, 'x1': 10.0, 'x2': 10.0, 'x3': 20.0}

        # 非标准形式：最小化和等式约束
        Min: x1 +  x2
        ST: 2x1 +  x2 = 12
            6x1 + 5x2 = 40
        >>> {key: float(value) for key, value in Tableau(np.array([
        ... [8, 6, 0, 0, 52],
        ... [1, 1, 0, 0, 0],
        ... [2, 1, 1, 0, 12],
        ... [6, 5, 0, 1, 40.],
        ... ]), 2, 2).run_simplex().items()}
        {'P': 7.0, 'x1': 5.0, 'x2': 2.0}


        # 在松弛变量上选取主元
        Max: 8x1 + 6x2
        ST:   x1 + 3x2 <= 33
             4x1 + 2x2 <= 48
             2x1 + 4x2 <= 48
              x1 +  x2 >= 10
             x1        >= 2
        >>> {key: float(value) for key, value in Tableau(np.array([
        ... [2, 1, 0, 0, 0, -1, -1, 0, 0, 12.0],
        ... [-8, -6, 0, 0, 0, 0, 0, 0, 0, 0.0],
        ... [1, 3, 1, 0, 0, 0, 0, 0, 0, 33.0],
        ... [4, 2, 0, 1, 0, 0, 0, 0, 0, 60.0],
        ... [2, 4, 0, 0, 1, 0, 0, 0, 0, 48.0],
        ... [1, 1, 0, 0, 0, -1, 0, 1, 0, 10.0],
        ... [1, 0, 0, 0, 0, 0, -1, 0, 1, 2.0]
        ... ]), 2, 2).run_simplex().items()} # doctest: +ELLIPSIS
        {'P': 132.0, 'x1': 12.000... 'x2': 5.999...}

        >>> original_maxiter = Tableau.maxiter
        >>> Tableau.maxiter = 0
        >>> Tableau(np.array([[-1, -1, 0, 0, 0], [1, 3, 1, 0, 4],
        ... [3, 1, 0, 1, 4.0]]), 2, 0).run_simplex()
        Traceback (most recent call last):
        ...
        ValueError: No convergence within 0 iterations; may be cycling/unbounded.
        >>> Tableau.maxiter = original_maxiter
        """
        # 防止单纯形算法循环
        for _ in range(Tableau.maxiter):
            # 每完成一个阶段就移除一个目标；两个阶段都完成后便不再有目标
            if not self.objectives:
                # 求最优解中各变量的值
                return self.interpret_tableau()

            row_idx, col_idx = self.find_pivot()

            # 若目标行中不再有负值
            if self.stop_iter:
                # 删除人工变量的列和行，并更新属性
                self.tableau = self.change_stage()
            else:
                self.tableau = self.pivot(row_idx, col_idx)
        msg = (
            f"No convergence within {Tableau.maxiter} iterations; "
            "may be cycling/unbounded."
        )
        raise ValueError(msg)

    def interpret_tableau(self) -> dict[str, float]:
        """给定最终单纯形表，将基本决策变量的对应值加入 `output_dict`。
        >>> {key: float(value) for key, value in Tableau(np.array([
        ... [0,0,0.875,0.375,5],
        ... [0,1,0.375,-0.125,1],
        ... [1,0,-0.125,0.375,1]
        ... ]),2, 0).interpret_tableau().items()}
        {'P': 5.0, 'x1': 1.0, 'x2': 1.0}
        """
        # P 等于最终单纯形表的右端项
        output_dict = {"P": abs(self.tableau[0, -1])}

        for i in range(self.n_vars):
            # 给出第 i 列非零元素的索引
            nonzero = np.nonzero(self.tableau[:, i])
            n_nonzero = len(nonzero[0])

            # 非零索引中的第一项
            nonzero_rowidx = nonzero[0][0]
            nonzero_val = self.tableau[nonzero_rowidx, i]

            # 若该列只有一个非零值，且该值为 1
            if n_nonzero == 1 and nonzero_val == 1:
                rhs_val = self.tableau[nonzero_rowidx, -1]
                output_dict[self.col_titles[i]] = rhs_val
        return output_dict


if __name__ == "__main__":
    import doctest

    doctest.testmod()
