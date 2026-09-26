# https://www.geeksforgeeks.org/solve-crossword-puzzle/


def is_valid(
    puzzle: list[list[str]], word: str, row: int, col: int, vertical: bool
) -> bool:
    """
    检查能否在给定位置放置单词。
    单元格为空或已有正确字母时有效
    （允许单词交叉并共享字母）。

    >>> puzzle = [['', '', '', ''], ['', '', '', ''],
    ...           ['', '', '', ''], ['', '', '', '']]
    >>> is_valid(puzzle, 'word', 0, 0, True)
    True
    >>> is_valid(puzzle, 'word', 0, 0, False)
    True
    >>> puzzle2 = [['w', '', ''], ['o', '', ''], ['r', '', ''], ['d', '', '']]
    >>> is_valid(puzzle2, 'word', 0, 0, True)
    True
    >>> is_valid(puzzle2, 'cat', 0, 0, True)
    False
    """
    rows, cols = len(puzzle), len(puzzle[0])
    for i, ch in enumerate(word):
        r, c = (row + i, col) if vertical else (row, col + i)
        if r >= rows or c >= cols:
            return False
        cell = puzzle[r][c]
        if cell not in ("", ch):
            return False
    return True


def place_word(
    puzzle: list[list[str]], word: str, row: int, col: int, vertical: bool
) -> None:
    """
    在字谜的给定位置放置单词。

    >>> puzzle = [['', '', '', ''], ['', '', '', ''],
    ...           ['', '', '', ''], ['', '', '', '']]
    >>> place_word(puzzle, 'word', 0, 0, True)
    >>> puzzle
    [['w', '', '', ''], ['o', '', '', ''], ['r', '', '', ''], ['d', '', '', '']]
    """
    for i, ch in enumerate(word):
        if vertical:
            puzzle[row + i][col] = ch
        else:
            puzzle[row][col + i] = ch


def remove_word(
    puzzle: list[list[str]],
    word: str,
    row: int,
    col: int,
    vertical: bool,
    snapshot: list[list[str]],
) -> None:
    """
    从字谜中移除单词，仅恢复放置前为空的
    单元格。保留与交叉单词共享的单元格。

    >>> puzzle = [['w', 'o', 'r', 'd'], ['', '', '', ''],
    ...           ['', '', '', ''], ['', '', '', '']]
    >>> snap = [['', 'o', 'r', 'd'], ['', '', '', ''],
    ...         ['', '', '', ''], ['', '', '', '']]
    >>> remove_word(puzzle, 'word', 0, 0, False, snap)
    >>> puzzle
    [['', 'o', 'r', 'd'], ['', '', '', ''], ['', '', '', ''], ['', '', '', '']]
    """
    for i in range(len(word)):
        r, c = (row + i, col) if vertical else (row, col + i)
        if snapshot[r][c] == "":
            puzzle[r][c] = ""


def solve_crossword(puzzle: list[list[str]], words: list[str]) -> bool:
    """
    使用回溯法求解填字游戏。
    优先尝试较长单词，以尽早缩小搜索空间。
    支持单词交叉（共享字母）。

    >>> puzzle = [['', '', '', ''], ['', '', '', ''],
    ...           ['', '', '', ''], ['', '', '', '']]
    >>> solve_crossword(puzzle, ['word', 'four', 'more', 'last'])
    True
    >>> puzzle2 = [['', '', '', ''], ['', '', '', ''],
    ...            ['', '', '', ''], ['', '', '', '']]
    >>> solve_crossword(puzzle2, ['word', 'four', 'more', 'paragraphs'])
    False
    """
    if not words:
        return True

    remaining = sorted(words, key=len, reverse=True)
    word, rest = remaining[0], remaining[1:]

    for row in range(len(puzzle)):
        for col in range(len(puzzle[0])):
            for vertical in (True, False):
                if is_valid(puzzle, word, row, col, vertical):
                    snapshot = [r[:] for r in puzzle]
                    place_word(puzzle, word, row, col, vertical)
                    if solve_crossword(puzzle, rest):
                        return True
                    remove_word(puzzle, word, row, col, vertical, snapshot)

    return False


if __name__ == "__main__":
    PUZZLE = [[""] * 3 for _ in range(3)]
    WORDS = ["cat", "dog", "car"]
    if solve_crossword(PUZZLE, WORDS):
        print("Solution found:")
        for row in PUZZLE:
            print(" ".join(cell or "." for cell in row))
    else:
        print("No solution found.")
