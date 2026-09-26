from __future__ import annotations


def solve_maze(
    maze: list[list[int]],
    source_row: int,
    source_column: int,
    destination_row: int,
    destination_column: int,
) -> list[list[int]]:
    """
    求解老鼠走迷宫问题。
    Parameters :
        - maze: 由零和一组成的二维矩阵。
        - source_row: 起点的行索引。
        - source_column: 起点的列索引。
        - destination_row: 终点的行索引。
        - destination_column: 终点的列索引。
    Returns:
        - solution: 若存在解，则为表示解路径的二维矩阵。
    Raises:
        - ValueError: 不存在解，或者起点或
            终点坐标无效时抛出。
    说明：
        在 n × n 矩阵表示的迷宫中，
        从指定的起始单元格出发，
        尝试到达目标单元格。
        迷宫由墙壁（1）和可通行路径（0）组成。
        可以通过自定义行列值，调整起点和终点的
        单元格位置。
    >>> maze = [[0, 1, 0, 1, 1],
    ...         [0, 0, 0, 0, 0],
    ...         [1, 0, 1, 0, 1],
    ...         [0, 0, 1, 0, 0],
    ...         [1, 0, 0, 1, 0]]
    >>> solve_maze(maze,0,0,len(maze)-1,len(maze)-1)    # doctest: +NORMALIZE_WHITESPACE
    [[0, 1, 1, 1, 1],
    [0, 0, 0, 0, 1],
    [1, 1, 1, 0, 1],
    [1, 1, 1, 0, 0],
    [1, 1, 1, 1, 0]]

    注意：
        输出迷宫中的零（0）表示从起点到终点的
        一条可能路径。

    >>> maze = [[0, 1, 0, 1, 1],
    ...         [0, 0, 0, 0, 0],
    ...         [0, 0, 0, 0, 1],
    ...         [0, 0, 0, 0, 0],
    ...         [0, 0, 0, 0, 0]]
    >>> solve_maze(maze,0,0,len(maze)-1,len(maze)-1)    # doctest: +NORMALIZE_WHITESPACE
    [[0, 1, 1, 1, 1],
    [0, 1, 1, 1, 1],
    [0, 1, 1, 1, 1],
    [0, 1, 1, 1, 1],
    [0, 0, 0, 0, 0]]

    >>> maze = [[0, 0, 0],
    ...         [0, 1, 0],
    ...         [1, 0, 0]]
    >>> solve_maze(maze,0,0,len(maze)-1,len(maze)-1)    # doctest: +NORMALIZE_WHITESPACE
    [[0, 0, 0],
    [1, 1, 0],
    [1, 1, 0]]

    >>> maze = [[1, 0, 0],
    ...         [0, 1, 0],
    ...         [1, 0, 0]]
    >>> solve_maze(maze,0,1,len(maze)-1,len(maze)-1)    # doctest: +NORMALIZE_WHITESPACE
    [[1, 0, 0],
    [1, 1, 0],
    [1, 1, 0]]

    >>> maze = [[1, 1, 0, 0, 1, 0, 0, 1],
    ...         [1, 0, 1, 0, 0, 1, 1, 1],
    ...         [0, 1, 0, 1, 0, 0, 1, 0],
    ...         [1, 1, 1, 0, 0, 1, 0, 1],
    ...         [0, 1, 0, 0, 1, 0, 1, 1],
    ...         [0, 0, 0, 1, 1, 1, 0, 1],
    ...         [0, 1, 0, 1, 0, 1, 1, 1],
    ...         [1, 1, 0, 0, 0, 0, 0, 1]]
    >>> solve_maze(maze,0,2,len(maze)-1,2)  # doctest: +NORMALIZE_WHITESPACE
    [[1, 1, 0, 0, 1, 1, 1, 1],
    [1, 1, 1, 0, 0, 1, 1, 1],
    [1, 1, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 0, 0, 1, 1, 1],
    [1, 1, 0, 0, 1, 1, 1, 1],
    [1, 1, 0, 1, 1, 1, 1, 1],
    [1, 1, 0, 1, 1, 1, 1, 1],
    [1, 1, 0, 1, 1, 1, 1, 1]]
    >>> maze = [[1, 0, 0],
    ...         [0, 1, 1],
    ...         [1, 0, 1]]
    >>> solve_maze(maze,0,1,len(maze)-1,len(maze)-1)
    Traceback (most recent call last):
        ...
    ValueError: No solution exists!

    >>> maze = [[0, 0],
    ...         [1, 1]]
    >>> solve_maze(maze,0,0,len(maze)-1,len(maze)-1)
    Traceback (most recent call last):
        ...
    ValueError: No solution exists!

    >>> maze = [[0, 1],
    ...         [1, 0]]
    >>> solve_maze(maze,2,0,len(maze)-1,len(maze)-1)
    Traceback (most recent call last):
        ...
    ValueError: Invalid source or destination coordinates

    >>> maze = [[1, 0, 0],
    ...         [0, 1, 0],
    ...         [1, 0, 0]]
    >>> solve_maze(maze,0,1,len(maze),len(maze)-1)
    Traceback (most recent call last):
        ...
    ValueError: Invalid source or destination coordinates
    """
    size = len(maze)
    # 检查起点和终点坐标是否无效。
    if not (0 <= source_row <= size - 1 and 0 <= source_column <= size - 1) or (
        not (0 <= destination_row <= size - 1 and 0 <= destination_column <= size - 1)
    ):
        raise ValueError("Invalid source or destination coordinates")
    # 创建 solution 对象以保存路径。
    solutions = [[1 for _ in range(size)] for _ in range(size)]
    solved = run_maze(
        maze, source_row, source_column, destination_row, destination_column, solutions
    )
    if solved:
        return solutions
    else:
        raise ValueError("No solution exists!")


def run_maze(
    maze: list[list[int]],
    i: int,
    j: int,
    destination_row: int,
    destination_column: int,
    solutions: list[list[int]],
) -> bool:
    """
    从 (i, j) 开始递归，向上、下、左、右
    四个方向之一移动。
    找到通往终点的路径时返回 True，否则返回 False。
    Parameters
        maze: 由零和一组成的二维矩阵。
        i, j : 矩阵坐标
        solutions: 解的二维矩阵。
    Returns:
        布尔值，找到路径时为 True，否则为 False。
    """
    size = len(maze)
    # 最终检查点。
    if i == destination_row and j == destination_column and maze[i][j] == 0:
        solutions[i][j] = 0
        return True

    lower_flag = (not i < 0) and (not j < 0)  # 检查下界
    upper_flag = (i < size) and (j < size)  # 检查上界

    if lower_flag and upper_flag:
        # 检查已访问位置和障碍位置。
        block_flag = (solutions[i][j]) and (not maze[i][j])
        if block_flag:
            # 标记已访问
            solutions[i][j] = 0

            # 检查各个方向
            if (
                run_maze(maze, i + 1, j, destination_row, destination_column, solutions)
                or run_maze(
                    maze, i, j + 1, destination_row, destination_column, solutions
                )
                or run_maze(
                    maze, i - 1, j, destination_row, destination_column, solutions
                )
                or run_maze(
                    maze, i, j - 1, destination_row, destination_column, solutions
                )
            ):
                return True

            solutions[i][j] = 1
            return False
    return False


if __name__ == "__main__":
    import doctest

    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)
