def points_to_polynomial(coordinates: list[list[int]]) -> str:
    """
    coordinates 是二维矩阵：[[x, y], [x, y], ...]
    表示要使用的点。

    >>> points_to_polynomial([])
    Traceback (most recent call last):
        ...
    ValueError: The program cannot work out a fitting polynomial.
    >>> points_to_polynomial([[]])
    Traceback (most recent call last):
        ...
    ValueError: The program cannot work out a fitting polynomial.
    >>> points_to_polynomial([[1, 0], [2, 0], [3, 0]])
    'f(x)=x^2*0.0+x^1*-0.0+x^0*0.0'
    >>> points_to_polynomial([[1, 1], [2, 1], [3, 1]])
    'f(x)=x^2*0.0+x^1*-0.0+x^0*1.0'
    >>> points_to_polynomial([[1, 3], [2, 3], [3, 3]])
    'f(x)=x^2*0.0+x^1*-0.0+x^0*3.0'
    >>> points_to_polynomial([[1, 1], [2, 2], [3, 3]])
    'f(x)=x^2*0.0+x^1*1.0+x^0*0.0'
    >>> points_to_polynomial([[1, 1], [2, 4], [3, 9]])
    'f(x)=x^2*1.0+x^1*-0.0+x^0*0.0'
    >>> points_to_polynomial([[1, 3], [2, 6], [3, 11]])
    'f(x)=x^2*1.0+x^1*-0.0+x^0*2.0'
    >>> points_to_polynomial([[1, -3], [2, -6], [3, -11]])
    'f(x)=x^2*-1.0+x^1*-0.0+x^0*-2.0'
    >>> points_to_polynomial([[1, 5], [2, 2], [3, 9]])
    'f(x)=x^2*5.0+x^1*-18.0+x^0*18.0'
    >>> points_to_polynomial([[1, 1], [1, 2], [1, 3]])
    'x=1'
    >>> points_to_polynomial([[1, 1], [2, 2], [2, 2]])
    Traceback (most recent call last):
        ...
    ValueError: The program cannot work out a fitting polynomial.
    >>> points_to_polynomial([[0, 1], [1, 2], [2, 5]])
    'f(x)=x^2*1.0+x^1*0.0+x^0*1.0'
    """
    if len(coordinates) == 0 or not all(len(pair) == 2 for pair in coordinates):
        raise ValueError("The program cannot work out a fitting polynomial.")

    if len({tuple(pair) for pair in coordinates}) != len(coordinates):
        raise ValueError("The program cannot work out a fitting polynomial.")

    set_x = {x for x, _ in coordinates}
    if len(set_x) == 1:
        return f"x={coordinates[0][0]}"

    if len(set_x) != len(coordinates):
        raise ValueError("The program cannot work out a fitting polynomial.")

    x = len(coordinates)

    # 将 x 及 x 的幂值放入矩阵
    matrix: list[list[float]] = [
        [
            coordinates[count_of_line][0] ** (x - (count_in_line + 1))
            for count_in_line in range(x)
        ]
        for count_of_line in range(x)
    ]

    # 将 y 值放入向量
    vector: list[float] = [coordinates[count_of_line][1] for count_of_line in range(x)]

    for count in range(x):
        # 仅在当前主元为零时交换（例如某个点的 x = 0），
        # 从而为正常输入保留现有的精确运算
        if matrix[count][count] == 0:
            pivot_row = max(
                range(count + 1, x), key=lambda row: abs(matrix[row][count])
            )
            if pivot_row == count or matrix[pivot_row][count] == 0:
                raise ValueError("The program cannot work out a fitting polynomial.")
            matrix[count], matrix[pivot_row] = matrix[pivot_row], matrix[count]
            vector[count], vector[pivot_row] = vector[pivot_row], vector[count]

        for number in range(x):
            if count == number:
                continue
            fraction = matrix[number][count] / matrix[count][count]
            for counting_columns, item in enumerate(matrix[count]):
    # 处理矩阵中的所有值
                matrix[number][counting_columns] -= item * fraction
    # 处理向量中的值
            vector[number] -= vector[count] * fraction

    # 构造解
    solution: list[str] = [
        str(vector[count] / matrix[count][count]) for count in range(x)
    ]

    solved = "f(x)="

    for count in range(x):
        remove_e: list[str] = solution[count].split("E")
        if len(remove_e) > 1:
            solution[count] = f"{remove_e[0]}*10^{remove_e[1]}"
        solved += f"x^{x - (count + 1)}*{solution[count]}"
        if count + 1 != x:
            solved += "+"

    return solved


if __name__ == "__main__":
    print(points_to_polynomial([]))
    print(points_to_polynomial([[]]))
    print(points_to_polynomial([[1, 0], [2, 0], [3, 0]]))
    print(points_to_polynomial([[1, 1], [2, 1], [3, 1]]))
    print(points_to_polynomial([[1, 3], [2, 3], [3, 3]]))
    print(points_to_polynomial([[1, 1], [2, 2], [3, 3]]))
    print(points_to_polynomial([[1, 1], [2, 4], [3, 9]]))
    print(points_to_polynomial([[1, 3], [2, 6], [3, 11]]))
    print(points_to_polynomial([[1, -3], [2, -6], [3, -11]]))
    print(points_to_polynomial([[1, 5], [2, 2], [3, 9]]))
