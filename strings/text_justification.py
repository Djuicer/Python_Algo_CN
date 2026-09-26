def text_justification(word: str, max_width: int) -> list:
    """
    格式化字符串，使每行恰好包含
    max_width 个字符，并实现左右两端对齐，
    返回对齐后的文本列表。

    示例 1：
    string = "This is an example of text justification."
    max_width = 16

    output = ['This    is    an',
              'example  of text',
              'justification.  ']

    >>> text_justification("This is an example of text justification.", 16)
    ['This    is    an', 'example  of text', 'justification.  ']

    示例 2：
    string = "Two roads diverged in a yellow wood"
    max_width = 16
    output = ['Two        roads',
              'diverged   in  a',
              'yellow wood     ']

    >>> text_justification("Two roads diverged in a yellow wood", 16)
    ['Two        roads', 'diverged   in  a', 'yellow wood     ']

    时间复杂度：O(m*n)
    空间复杂度：O(m*n)
    """

    # 按空格将字符串拆分为字符串列表
    words = word.split()

    def justify(line: list, width: int, max_width: int) -> str:
        overall_spaces_count = max_width - width
        words_count = len(line)
        if len(line) == 1:
            # 若行中只有一个单词，
            # 则在行尾补入 overall_spaces_count 个空格
            return line[0] + " " * overall_spaces_count
        else:
            spaces_to_insert_between_words = words_count - 1
            # num_spaces_between_words_list[i] 表示在
            # line[i] 处的单词后插入
            # num_spaces_between_words_list[i] 个空格
            num_spaces_between_words_list = spaces_to_insert_between_words * [
                overall_spaces_count // spaces_to_insert_between_words
            ]
            spaces_count_in_locations = (
                overall_spaces_count % spaces_to_insert_between_words
            )
            # 从左侧单词开始轮流分配空格
            for i in range(spaces_count_in_locations):
                num_spaces_between_words_list[i] += 1
            aligned_words_list = []
            for i in range(spaces_to_insert_between_words):
                # 添加单词
                aligned_words_list.append(line[i])
                # 添加所需空格
                aligned_words_list.append(num_spaces_between_words_list[i] * " ")
            # 将最后一个单词加入句子
            aligned_words_list.append(line[-1])
            # 连接对齐后的单词列表，形成两端对齐的一行
            return "".join(aligned_words_list)

    answer = []
    line: list[str] = []
    width = 0
    for inner_word in words:
        if width + len(inner_word) + len(line) <= max_width:
            # 持续添加单词，直到达到 max_width
            # width = 所有单词长度之和（不含 overall_spaces_count）
            # len(inner_word) = 当前 inner_word 的长度
            # len(line) = 单词之间需要插入的 overall_spaces_count 数量
            line.append(inner_word)
            width += len(inner_word)
        else:
            # 对齐该行并加入结果
            answer.append(justify(line, width, max_width))
            # 重置新行和宽度
            line, width = [inner_word], len(inner_word)
    remaining_spaces = max_width - width - len(line)
    answer.append(" ".join(line) + (remaining_spaces + 1) * " ")
    return answer


if __name__ == "__main__":
    from doctest import testmod

    testmod()
