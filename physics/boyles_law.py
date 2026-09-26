"""
标题：玻意耳定律的实现。

说明：
    玻意耳定律又称 Boyle-Mariotte 定律或 Mariotte 定律（尤其在法国），指出
    质量和温度固定的气体所产生的压强与其占据的体积成反比。

    对于质量和温度恒定的气体，体积与压强的关系可表示为：

    P ∝ (1/V)

    其中 P 为气体产生的压强，V 为气体占据的体积。引入常数 k 可将该比例关系
    转换为方程。

    P = k*(1/V) ⇒ PV = k

    玻意耳定律指出，给定质量的密闭气体温度恒定时，其压强与体积的乘积也
    保持恒定。比较同一物质在两组不同条件下的状态时，该定律可表示为：

    P1V1 = P2V2

    其中：

    P1 为气体的初始压强，单位为帕斯卡 (P)
    V1 为气体的初始体积，单位为升 (L)
    P2 为气体的最终压强，单位为帕斯卡 (P)
    V2 为气体的最终体积，单位为升 (L)

    当容器体积减小，而气体的量和绝对温度保持不变时，可用该方程预测气体
    对容器壁压强的增加。

来源：
    https://en.wikipedia.org/wiki/Boyle%27s_law
    https://byjus.com/chemistry/boyles-law/
"""

valid_variables: list[str] = ["v1", "v2", "p1", "p2"]


def check_validity(values: dict[str, float]) -> None:
    """

    函数接收字典作为输入；若输入有效，则不返回任何内容。

    >>> check_validity({})
    Traceback (most recent call last):
        ...
    ValueError: Invalid input expected 3 items, got 0

    >>> check_validity({'v1':2,'v2':4,'k':6})
    Traceback (most recent call last):
        ...
    ValueError: Invalid input k is not a valid variable

    >>> check_validity({'v1':2,'v2':4,'p1':-6})
    Traceback (most recent call last):
        ...
    ValueError: Invalid input p1 must be greater than 0

    >>> check_validity({'v1':2,'v2':4,'p1':6})

    """
    if len(values) != 3:
        msg = f"Invalid input expected {3} items, got {len(values)}"
        raise ValueError(msg)
    for value, val in values.items():
        if value not in valid_variables:
            msg = f"Invalid input {value} is not a valid variable"
            raise ValueError(msg)
        if val <= 0:
            msg = f"Invalid input {value} must be greater than 0"
            raise ValueError(msg)


def find_target_variable(values: dict[str, float]) -> str:
    """

    获取需要利用玻意耳定律求值的有效目标变量。
    函数接收字典作为输入并返回字符串。

    >>> find_target_variable({})
    Traceback (most recent call last):
        ...
    ValueError: Invalid input expected 3 items, got 0

    >>> find_target_variable({'v1':1,'v2':2,'p2':4})
    'p1'

    >>> find_target_variable({'v1':1,'v2':2,'k':4})
    Traceback (most recent call last):
        ...
    ValueError: Invalid input k is not a valid variable

    >>> find_target_variable({'v1':1,'v2':-2,'p2':4})
    Traceback (most recent call last):
        ...
    ValueError: Invalid input v2 must be greater than 0

    """
    check_validity(values)
    for variable in valid_variables:
        if variable not in values:
            return variable
    raise ValueError("Input is invalid")


def boyles_law(values: dict[str, float]) -> dict[str, str]:
    """

    使用玻意耳定律计算未知的压强或体积。函数接收包含相应压强和体积值的
    字典作为输入，计算并返回所需值。

    >>> boyles_law({'p1':2,'v2':1})
    Traceback (most recent call last):
        ...
    ValueError: Invalid input expected 3 items, got 2

    >>> boyles_law({})
    Traceback (most recent call last):
        ...
    ValueError: Invalid input expected 3 items, got 0

    >>> boyles_law({'p1':2,'v2':1, 'k':6})
    Traceback (most recent call last):
        ...
    ValueError: Invalid input k is not a valid variable

    >>> boyles_law({'p1':2,'v2':1, 'v1':-6})
    Traceback (most recent call last):
        ...
    ValueError: Invalid input v1 must be greater than 0

    >>> boyles_law({'p1':100,'v2':150, 'v1':120})
    {'p2': '80.0 Pa'}

    >>> boyles_law({'p1':10,'v1':20, 'p2':20})
    {'v2': '10.0 L'}

    >>> boyles_law({'v1':13,'p2':17, 'v2':19})
    {'p1': '24.846 Pa'}

    >>> boyles_law({'v2':27,'p1':25, 'p2':29})
    {'v1': '31.32 L'}

    """
    check_validity(values)
    target = find_target_variable(values)
    float_precision = ".3f"
    if target == "p1":
        p1 = float(
            format((values["p2"] * values["v2"]) / values["v1"], float_precision)
        )
        return {"p1": f"{p1} Pa"}
    elif target == "v1":
        v1 = float(
            format((values["p2"] * values["v2"]) / values["p1"], float_precision)
        )
        return {"v1": f"{v1} L"}
    elif target == "p2":
        p2 = float(
            format((values["p1"] * values["v1"]) / values["v2"], float_precision)
        )
        return {"p2": f"{p2} Pa"}
    else:
        v2 = float(
            format((values["p1"] * values["v1"]) / values["p2"], float_precision)
        )
        return {"v2": f"{v2} L"}


if __name__ == "__main__":
    import doctest

    doctest.testmod()
