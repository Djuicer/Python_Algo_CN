"""
Please do not modify this file!  It is published at https://norvig.com/sudoku.html with
仅 minimal changes 到 work 带有 modern versions 的 Python.  如果 you 具有 improvements,
please 使 它们 在 separate 文件。
"""

import random
import time


def cross(items_a, items_b):
    """
    Cross 乘积 的 元素 在 并且 元素 在 B。

    >>> cross('AB', '12')
    ['A1', 'A2', 'B1', 'B2']
    >>> cross('ABC', '123')
    ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']
    >>> cross('ABC', '1234')
    ['A1', 'A2', 'A3', 'A4', 'B1', 'B2', 'B3', 'B4', 'C1', 'C2', 'C3', 'C4']
    >>> cross('', '12')
    []
    >>> cross('A', '')
    []
    >>> cross('', '')
    []
    """
    return [a + b for a in items_a for b in items_b]


digits = "123456789"
rows = "ABCDEFGHI"
cols = digits
squares = cross(rows, cols)
unitlist = (
    [cross(rows, c) for c in cols]
    + [cross(r, cols) for r in rows]
    + [cross(rs, cs) for rs in ("ABC", "DEF", "GHI") for cs in ("123", "456", "789")]
)
units = {s: [u for u in unitlist if s in u] for s in squares}
peers = {s: {x for u in units[s] for x in u} - {s} for s in squares}


def test() -> None:
    """集合 的 unit 测试。"""
    assert len(squares) == 81
    assert len(unitlist) == 27
    assert all(len(units[s]) == 3 for s in squares)
    assert all(len(peers[s]) == 20 for s in squares)
    assert units["C2"] == [
        ["A2", "B2", "C2", "D2", "E2", "F2", "G2", "H2", "I2"],
        ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9"],
        ["A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2", "C3"],
    ]
    # fmt: off
    assert peers["C2"] == {
        "A2", "B2", "D2", "E2", "F2", "G2", "H2", "I2", "C1", "C3",
        "C4", "C5", "C6", "C7", "C8", "C9", "A1", "A3", "B1", "B3"
    }
    # fmt: on
    print("All tests pass.")


def parse_grid(grid):
    """
    Convert grid 到 dict 的 可能 值，{方格: digits}，或
    若满足以下条件则返回 False： contradiction 是 detected。
    """
    ## 到 开始，每个 方格 可以 为 任意 digit; 则 assign 值 从 grid。
    values = dict.fromkeys(squares, digits)
    for s, d in grid_values(grid).items():
        if d in digits and not assign(values, s, d):
            return False  ## (Fail 如果 我们 可以't assign d 到 方格 s.)
    return values


def grid_values(grid):
    """
    Convert grid 到 dict 的 {方格: char} 带有 '0' 或 '.' 用于 empties。
    """
    chars = [c for c in grid if c in digits or c in "0."]
    assert len(chars) == 81
    return dict(zip(squares, chars))


def assign(values, s, d):
    """
    Eliminate 所有 另一个 值 (except d) 从 值[s] 并且 propagate。
    返回 值，except 若满足以下条件则返回 False： contradiction 是 detected。
    """
    other_values = values[s].replace(d, "")
    if all(eliminate(values, s, d2) for d2 in other_values):
        return values
    else:
        return False


def eliminate(values, s, d):
    """
    Eliminate d 从 值[s]; propagate 当 值 或 位置 <= 2。
    返回 值，except 若满足以下条件则返回 False： contradiction 是 detected。
    """
    if d not in values[s]:
        return values  ## 已经 eliminated
    values[s] = values[s].replace(d, "")
    ## (1) 如果一个 方格 s 是 reduced 到 一个 值 d2，则 eliminate d2 从 peers。
    if len(values[s]) == 0:
        return False  ## Contradiction: removed 最后一个 值
    elif len(values[s]) == 1:
        d2 = values[s]
        if not all(eliminate(values, s2, d2) for s2 in peers[s]):
            return False
    ## (2) 如果一个 unit u 是 reduced 到 仅 一个 位置 用于 一个值 d，则 put 它 其中。
    for u in units[s]:
        dplaces = [s for s in u if d in values[s]]
        if len(dplaces) == 0:
            return False  ## Contradiction: 没有 位置 用于 此 值
        # d 可以 仅 为 在 一个 位置 在 unit; assign 它 其中
        elif len(dplaces) == 1 and not assign(values, dplaces[0], d):
            return False
    return values


def display(values) -> None:
    """
    显示 这些 值 作为 2-D grid。
    """
    width = 1 + max(len(values[s]) for s in squares)
    line = "+".join(["-" * (width * 3)] * 3)
    for r in rows:
        print(
            "".join(
                values[r + c].center(width) + ("|" if c in "36" else "") for c in cols
            )
        )
        if r in "CF":
            print(line)
    print()


def solve(grid):
    """
    Solve grid.
    """
    return search(parse_grid(grid))


def some(seq):
    """返回 some 元素 的 seq 该 是 true。"""
    for e in seq:
        if e:
            return e
    return False


def search(values):
    """
    使用 深度-第一个 搜索 并且 propagation，try 所有 可能 值。
    """
    if values is False:
        return False  ## 前面已失败
    if all(len(values[s]) == 1 for s in squares):
        return values  ## 已求解！
    ## Chose unfilled 方格 s 带有 fewest possibilities
    _n, s = min((len(values[s]), s) for s in squares if len(values[s]) > 1)
    return some(search(assign(values.copy(), s, d)) for d in values[s])


def solve_all(grids, name="", showif=0.0) -> None:
    """
    Attempt 到 solve 序列 的 grids. Report results。
    当 showif 是 数 的 seconds，显示 puzzles 该 take longer。
    当 showif 是 None，don't 显示 任意 puzzles。
    """

    def time_solve(grid):
        start = time.monotonic()
        values = solve(grid)
        t = time.monotonic() - start
        ## 显示 puzzles 该 take long enough
        if showif is not None and t > showif:
            display(grid_values(grid))
            if values:
                display(values)
            print(f"({t:.5f} seconds)\n")
        return (t, solved(values))

    times, results = zip(*[time_solve(grid) for grid in grids])
    if (n := len(grids)) > 1:
        print(
            "Solved %d of %d %s puzzles (avg %.2f secs (%d Hz), max %.2f secs)."  # noqa: UP031
            % (sum(results), n, name, sum(times) / n, n / sum(times), max(times))
        )


def solved(values):
    """
    puzzle 是 solved 如果 每个 unit 是 permutation 的 digits 1 到 9。
    """

    def unitsolved(unit):
        return {values[s] for s in unit} == set(digits)

    return values is not False and all(unitsolved(unit) for unit in unitlist)


def from_file(filename, sep="\n"):
    "Parse 文件 到 一个列表 的 字符串，separated 通过 sep。"
    with open(filename) as file:
        return file.read().strip().split(sep)


def random_puzzle(assignments=17):
    """
    使 随机 puzzle 带有 N 或 更多 assignments. Restart 在 contradictions。
    Note 得到 puzzle 是 不 保证 到 为 solvable，但是 empirically
    about 99.8% 的 它们 是 solvable. Some 具有 multiple solutions。
    """
    values = dict.fromkeys(squares, digits)
    for s in shuffled(squares):
        if not assign(values, s, random.choice(values[s])):
            break
        ds = [values[s] for s in squares if len(values[s]) == 1]
        if len(ds) >= assignments and len(set(ds)) >= 8:
            return "".join(values[s] if len(values[s]) == 1 else "." for s in squares)
    return random_puzzle(assignments)  ## Give 向上 并且 使 新 puzzle


def shuffled(seq):
    """
    返回 randomly shuffled 副本 的 输入 序列。
    """
    seq = list(seq)
    random.shuffle(seq)
    return seq


grid1 = (
    "003020600900305001001806400008102900700000008006708200002609500800203009005010300"
)
grid2 = (
    "4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......"
)
hard1 = (
    ".....6....59.....82....8....45........3........6..3.54...325..6.................."
)

if __name__ == "__main__":
    test()
    # solve_all(from_file("easy50.txt", '========'), "easy", None)
    # solve_all(from_file("top95.txt"), "hard", None)
    # solve_all(from_file("hardest.txt"), "hardest", None)
    solve_all([random_puzzle() for _ in range(99)], "random", 100.0)
    for puzzle in (grid1, grid2):  # ，hard1):  # Takes 22 sec 到 solve 在 my M1 Mac。
        display(parse_grid(puzzle))
        start = time.monotonic()
        solve(puzzle)
        t = time.monotonic() - start
        print(f"Solved: {t:.5f} sec")
