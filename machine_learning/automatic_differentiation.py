"""
自动微分（Automatic Differentiation）反向模式的演示。

Reference: https://en.wikipedia.org/wiki/Automatic_differentiation

Author: Poojan Smart
Email: smrtpoojan@gmail.com
"""

from __future__ import annotations

from enum import Enum
from types import TracebackType
from typing import Any, Self

import numpy as np


class OpType(Enum):
    """
    表示 Variable 为计算梯度所支持的操作列表。
    """

    ADD = 0
    SUB = 1
    MUL = 2
    DIV = 3
    MATMUL = 4
    POWER = 5
    NOOP = 6


class Variable:
    """
    表示封装 NumPy 数组的 n 维对象，将在该数组上执行运算并计算梯度。

    示例：
    >>> Variable(5.0)
    Variable(5.0)
    >>> Variable([5.0, 2.9])
    Variable([5.  2.9])
    >>> Variable([5.0, 2.9]) + Variable([1.0, 5.5])
    Variable([6.  8.4])
    >>> Variable([[8.0, 10.0]])
    Variable([[ 8. 10.]])
    """

    def __init__(self, value: Any) -> None:
        self.value = np.array(value)

    # 指向以该 Variable 为输入的操作
        self.param_to: list[Operation] = []
    # 指向以该 Variable 为输出的操作
        self.result_of: Operation = Operation(OpType.NOOP)

    def __repr__(self) -> str:
        return f"Variable({self.value})"

    def to_ndarray(self) -> np.ndarray:
        return self.value

    def __add__(self, other: Variable) -> Variable:
        result = Variable(self.value + other.value)

        with GradientTracker() as tracker:
        # 如果启用了跟踪器，则更新计算图
            if tracker.enabled:
                tracker.append(OpType.ADD, params=[self, other], output=result)
        return result

    def __sub__(self, other: Variable) -> Variable:
        result = Variable(self.value - other.value)

        with GradientTracker() as tracker:
            # if tracker is enabled, computation graph will be updated
            if tracker.enabled:
                tracker.append(OpType.SUB, params=[self, other], output=result)
        return result

    def __mul__(self, other: Variable) -> Variable:
        result = Variable(self.value * other.value)

        with GradientTracker() as tracker:
            # if tracker is enabled, computation graph will be updated
            if tracker.enabled:
                tracker.append(OpType.MUL, params=[self, other], output=result)
        return result

    def __truediv__(self, other: Variable) -> Variable:
        result = Variable(self.value / other.value)

        with GradientTracker() as tracker:
            # if tracker is enabled, computation graph will be updated
            if tracker.enabled:
                tracker.append(OpType.DIV, params=[self, other], output=result)
        return result

    def __matmul__(self, other: Variable) -> Variable:
        result = Variable(self.value @ other.value)

        with GradientTracker() as tracker:
            # if tracker is enabled, computation graph will be updated
            if tracker.enabled:
                tracker.append(OpType.MATMUL, params=[self, other], output=result)
        return result

    def __pow__(self, power: int) -> Variable:
        result = Variable(self.value**power)

        with GradientTracker() as tracker:
            # if tracker is enabled, computation graph will be updated
            if tracker.enabled:
                tracker.append(
                    OpType.POWER,
                    params=[self],
                    output=result,
                    other_params={"power": power},
                )
        return result

    def add_param_to(self, param_to: Operation) -> None:
        self.param_to.append(param_to)

    def add_result_of(self, result_of: Operation) -> None:
        self.result_of = result_of


class Operation:
    """
    表示一个或两个 Variable 对象之间的运算。Operation 对象包含运算类型、
    指向输入 Variable 对象的引用，以及指向运算结果 Variable 的引用。
    """

    def __init__(
        self,
        op_type: OpType,
        other_params: dict | None = None,
    ) -> None:
        self.op_type = op_type
        self.other_params = {} if other_params is None else other_params

    def add_params(self, params: list[Variable]) -> None:
        self.params = params

    def add_output(self, output: Variable) -> None:
        self.output = output

    def __eq__(self, value) -> bool:
        return self.op_type == value if isinstance(value, OpType) else False


class GradientTracker:
    """
    包含基于计算图求 Variable 偏导数的方法。

    示例：

    >>> with GradientTracker() as tracker:
    ...     a = Variable([2.0, 5.0])
    ...     b = Variable([1.0, 2.0])
    ...     m = Variable([1.0, 2.0])
    ...     c = a + b
    ...     d = a * b
    ...     e = c / d
    >>> tracker.gradient(e, a)
    array([-0.25, -0.04])
    >>> tracker.gradient(e, b)
    array([-1.  , -0.25])
    >>> tracker.gradient(e, m) is None
    True

    >>> with GradientTracker() as tracker:
    ...     a = Variable([[2.0, 5.0]])
    ...     b = Variable([[1.0], [2.0]])
    ...     c = a @ b
    >>> tracker.gradient(c, a)
    array([[1., 2.]])
    >>> tracker.gradient(c, b)
    array([[2.],
           [5.]])

    >>> with GradientTracker() as tracker:
    ...     a = Variable([[2.0, 5.0]])
    ...     b = a ** 3
    >>> tracker.gradient(b, a)
    array([[12., 75.]])
    """

    instance = None

    def __new__(cls) -> Self:
        """
        创建类对象时执行；若对象已经创建则直接返回。本类采用单例设计模式。
        """
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        self.enabled = False

    def __enter__(self) -> Self:
        self.enabled = True
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.enabled = False

    def append(
        self,
        op_type: OpType,
        params: list[Variable],
        output: Variable,
        other_params: dict | None = None,
    ) -> None:
        """
        将 Operation 对象添加到相关 Variable 对象，以创建用于计算梯度的计算图。

        参数：
            op_type：运算类型
            params：运算的输入参数
            output：运算的输出变量
        """
        operation = Operation(op_type, other_params=other_params)
        param_nodes = []
        for param in params:
            param.add_param_to(operation)
            param_nodes.append(param)
        output.add_result_of(operation)

        operation.add_params(param_nodes)
        operation.add_output(output)

    def gradient(self, target: Variable, source: Variable) -> np.ndarray | None:
        """
        反向累积偏导数，计算目标变量相对于源变量的梯度。

        参数：
            target：要计算梯度的目标变量。
            source：计算梯度所参照的源变量。

        返回：
            源变量相对于目标变量的梯度
        """

        # 相对于目标变量的偏导数
        partial_deriv: dict[Variable, np.ndarray] = {}
        partial_deriv[target] = np.ones_like(target.to_ndarray())

        # 遍历计算图中的每个操作
        operation_queue = [target.result_of]
        while len(operation_queue) > 0:
            operation = operation_queue.pop()
            for param in operation.params:
            # 根据链式法则，将变量相对于目标的偏导数相乘
                dparam_doutput = self.derivative(param, operation)
                dparam_dtarget = dparam_doutput * partial_deriv[operation.output]
                partial_deriv[param] = (
                    partial_deriv.get(param, np.zeros_like(dparam_dtarget))
                    + dparam_dtarget
                )

                if param.result_of and param.result_of != OpType.NOOP:
                    operation_queue.append(param.result_of)

        return partial_deriv.get(source)

    def derivative(self, param: Variable, operation: Operation) -> np.ndarray:
        """
        计算给定运算或函数的导数

        参数：
            param：要进行求导的变量
            operation：对输入变量执行的函数

        返回：
            输入变量相对于运算输出的导数
        """
        params = operation.params

        if operation == OpType.ADD:
            return np.ones_like(params[0].to_ndarray(), dtype=np.float64)
        if operation == OpType.SUB:
            if params[0] == param:
                return np.ones_like(params[0].to_ndarray(), dtype=np.float64)
            return -np.ones_like(params[1].to_ndarray(), dtype=np.float64)
        if operation == OpType.MUL:
            return (
                params[1].to_ndarray().T
                if params[0] == param
                else params[0].to_ndarray().T
            )
        if operation == OpType.DIV:
            if params[0] == param:
                return 1 / params[1].to_ndarray()
            return -params[0].to_ndarray() / (params[1].to_ndarray() ** 2)
        if operation == OpType.MATMUL:
            return (
                params[1].to_ndarray().T
                if params[0] == param
                else params[0].to_ndarray().T
            )
        if operation == OpType.POWER:
            power = operation.other_params["power"]
            return power * (params[0].to_ndarray() ** (power - 1))

        err_msg = f"invalid operation type: {operation.op_type}"
        raise ValueError(err_msg)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
