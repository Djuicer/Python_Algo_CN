"""
基于矩阵的游戏脚本
=========================
本脚本实现一个基于矩阵的游戏，玩家与元素网格进行交互。主要目标是：
- 从所选位置识别类型相同的相连元素。
- 移除这些元素，通过模拟重力调整矩阵，并重新排列空列。
- 根据每一步移除的元素数量计算并显示分数。

函数：
-----------
1. `find_repeat`：查找类型相同的所有相连元素。
2. `increment_score`：计算给定移动的得分。
3. `move_x`：模拟列中的重力。
4. `move_y`：当一列变空时，通过将各列左移来重组矩阵。
5. `play`：执行一次移动，更新矩阵并返回得分。

输入格式：
--------------
1. 矩阵大小（`lines`）：指定矩阵大小（N x N）的整数。
2. 矩阵内容（`matrix`）：矩阵的各行，每行由字符组成。
3. 移动次数（`movs`）：表示移动次数的整数。
4. 移动列表（`movements`）：以逗号分隔、表示各次移动坐标的字符串。

(0,0) 位置从最左列到最右列、从下方行到上方行进行定位。


输入示例：
---------------
4
RRBG
RBBG
YYGG
XYGG
2
0 1,1 1

示例中 (0,0) = X

输出：
--------
脚本在处理完所有移动后输出总分。

用法：
-------
运行脚本，并按提示提供所需输入。

"""


def validate_matrix_size(size: int) -> None:
    """
    >>> validate_matrix_size(-1)
    Traceback (most recent call last):
        ...
    ValueError: Matrix size must be a positive integer.
    """
    if not isinstance(size, int) or size <= 0:
        raise ValueError("Matrix size must be a positive integer.")


def validate_matrix_content(matrix: list[str], size: int) -> None:
    """
    验证矩阵中的元素数量是否与给定大小匹配。

    >>> validate_matrix_content(['aaaa', 'aaaa', 'aaaa', 'aaaa'], 3)
    Traceback (most recent call last):
        ...
    ValueError: The matrix dont match with size.
    >>> validate_matrix_content(['aa%', 'aaa', 'aaa'], 3)
    Traceback (most recent call last):
        ...
    ValueError: Matrix rows can only contain letters and numbers.
    >>> validate_matrix_content(['aaa', 'aaa', 'aaaa'], 3)
    Traceback (most recent call last):
        ...
    ValueError: Each row in the matrix must have exactly 3 characters.
    """
    print(matrix)
    if len(matrix) != size:
        raise ValueError("The matrix dont match with size.")
    for row in matrix:
        if len(row) != size:
            msg = f"Each row in the matrix must have exactly {size} characters."
            raise ValueError(msg)
        if not all(char.isalnum() for char in row):
            raise ValueError("Matrix rows can only contain letters and numbers.")


def validate_moves(moves: list[tuple[int, int]], size: int) -> None:
    """
    >>> validate_moves([(1, 2), (-1, 0)], 3)
    Traceback (most recent call last):
        ...
    ValueError: Move is out of bounds for a matrix.
    """
    for move in moves:
        x, y = move
        if not (0 <= x < size and 0 <= y < size):
            raise ValueError("Move is out of bounds for a matrix.")


def parse_moves(input_str: str) -> list[tuple[int, int]]:
    """
    >>> parse_moves("0 1, 1 1")
    [(0, 1), (1, 1)]
    >>> parse_moves("0 1, 1 1, 2")
    Traceback (most recent call last):
        ...
    ValueError: Each move must have exactly two numbers.
    >>> parse_moves("0 1, 1 1, 2 4 5 6")
    Traceback (most recent call last):
        ...
    ValueError: Each move must have exactly two numbers.
    """
    moves = []
    for pair in input_str.split(","):
        parts = pair.strip().split()
        if len(parts) != 2:
            raise ValueError("Each move must have exactly two numbers.")
        x, y = map(int, parts)
        moves.append((x, y))
    return moves


def find_repeat(
    matrix_g: list[list[str]], row: int, column: int, size: int
) -> set[tuple[int, int]]:
    """
    从给定位置查找类型相同的所有相连元素。

    >>> find_repeat([['A', 'B', 'A'], ['A', 'B', 'A'], ['A', 'A', 'A']], 0, 0, 3)
    {(1, 2), (2, 1), (0, 0), (2, 0), (0, 2), (2, 2), (1, 0)}
    >>> find_repeat([['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']], 1, 1, 3)
    set()
    """

    column = size - 1 - column
    visited = set()
    repeated = set()

    if (color := matrix_g[column][row]) != "-":

        def dfs(row_n: int, column_n: int) -> None:
            if row_n < 0 or row_n >= size or column_n < 0 or column_n >= size:
                return
            if (row_n, column_n) in visited:
                return
            visited.add((row_n, column_n))
            if matrix_g[row_n][column_n] == color:
                repeated.add((row_n, column_n))
                dfs(row_n - 1, column_n)
                dfs(row_n + 1, column_n)
                dfs(row_n, column_n - 1)
                dfs(row_n, column_n + 1)

        dfs(column, row)

    return repeated


def increment_score(count: int) -> int:
    """
    根据一次移动所移除的元素数量计算得分。

    >>> increment_score(3)
    6
    >>> increment_score(0)
    0
    """
    return int(count * (count + 1) / 2)


def move_x(matrix_g: list[list[str]], column: int, size: int) -> list[list[str]]:
    """
    在指定列中模拟重力。

    >>> move_x([['-', 'A'], ['-', '-'], ['-', 'C']], 1, 2)
    [['-', '-'], ['-', 'A'], ['-', 'C']]
    """

    new_list = []

    for row in range(size):
        if matrix_g[row][column] != "-":
            new_list.append(matrix_g[row][column])
        else:
            new_list.insert(0, matrix_g[row][column])
    for row in range(size):
        matrix_g[row][column] = new_list[row]
    return matrix_g


def move_y(matrix_g: list[list[str]], size: int) -> list[list[str]]:
    """
    当整列变空时，将所有列向左移动。

    >>> move_y([['-', 'A'], ['-', '-'], ['-', 'C']], 2)
    [['A', '-'], ['-', '-'], ['-', 'C']]
    """

    empty_columns = []

    for column in range(size - 1, -1, -1):
        if all(matrix_g[row][column] == "-" for row in range(size)):
            empty_columns.append(column)

    for column in empty_columns:
        for col in range(column + 1, size):
            for row in range(size):
                matrix_g[row][col - 1] = matrix_g[row][col]
        for row in range(size):
            matrix_g[row][-1] = "-"

    return matrix_g


def play(
    matrix_g: list[list[str]], pos_x: int, pos_y: int, size: int
) -> tuple[list[list[str]], int]:
    """
    处理一次移动，更新矩阵并计算得分。

    >>> play([['R', 'G'], ['R', 'G']], 0, 0, 2)
    ([['G', '-'], ['G', '-']], 3)
    """

    same_colors = find_repeat(matrix_g, pos_x, pos_y, size)

    if len(same_colors) != 0:
        for pos in same_colors:
            matrix_g[pos[0]][pos[1]] = "-"
        for column in range(size):
            matrix_g = move_x(matrix_g, column, size)

        matrix_g = move_y(matrix_g, size)

    return (matrix_g, increment_score(len(same_colors)))


def process_game(size: int, matrix: list[str], moves: list[tuple[int, int]]) -> int:
    """处理给定矩阵和移动的游戏逻辑。

    参数：
        size (int): 游戏面板大小。
        matrix (List[str]): 初始游戏矩阵。
        moves (List[Tuple[int, int]]): 以 (x, y) 坐标表示的移动列表。

    返回：
        int: 获得的总分。
    >>> process_game(3, ['aaa', 'bbb', 'ccc'], [(0, 0)])
    6
    """

    game_matrix = [list(row) for row in matrix]
    total_score = 0

    for move in moves:
        pos_x, pos_y = move
        game_matrix, score = play(game_matrix, pos_x, pos_y, size)
        total_score += score

    return total_score


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)
    try:
        size = int(input("Enter the size of the matrix: "))
        validate_matrix_size(size)
        print(f"Enter the {size} rows of the matrix:")
        matrix = [input(f"Row {i + 1}: ") for i in range(size)]
        validate_matrix_content(matrix, size)
        moves_input = input("Enter the moves (e.g., '0 0, 1 1'): ")
        moves = parse_moves(moves_input)
        validate_moves(moves, size)
        score = process_game(size, matrix, moves)
        print(f"Total score: {score}")
    except ValueError as e:
        print(f"{e}")
