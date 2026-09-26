def min_window(search_str: str, target_letters: str) -> str:
    """
    给定待搜索字符串，以及另一个表示目标 char_dict 的字符串，
    返回搜索字符串中包含所有目标 char_dict 的
    最短子串。

    此实现对我在 LeetCode 上的
    “Minimum Window Substring”题目解法略作修改。
    https://leetcode.com/problems/minimum-window-substring/description/

    >>> min_window("Hello World", "lWl")
    'llo W'
    >>> min_window("Hello World", "f")
    ''

    使用滑动窗口，交替执行以下操作：
    向右移动窗口末端，直到窗口包含所有目标 char_dict；
    再向右移动窗口起点，直到窗口
    不再包含每个目标字符。

    时间复杂度：O(target_count + search_len) ->
        对于 search_str 中的每个字符，
        最多查询字典两次。

    空间复杂度：O(search_len) ->
        额外空间主要用于根据搜索字符串
        构建字典。
    """

    target_count = len(target_letters)
    search_len = len(search_str)

    # 根据字符串长度判断无法匹配时，直接返回。
    if search_len < target_count:
        return ""

    # 构建字典，记录 target_letters 中每个字母的数量
    char_dict = {}
    for ch in target_letters:
        if ch not in char_dict:
            char_dict[ch] = 1
        else:
            char_dict[ch] += 1

    # 初始化窗口
    window_start = 0
    window_end = 0

    exists = False
    min_window_len = search_len + 1

    # 开始滑动窗口算法
    while window_end < search_len:
        # 向右移动窗口末端，直到包含所有待搜索字符
        while target_count > 0 and window_end < search_len:
            cur = search_str[window_end]
            if cur in char_dict:
                char_dict[cur] -= 1
                if char_dict[cur] >= 0:
                    target_count -= 1
            window_end += 1
        temp = window_end - window_start

        # 检查窗口是否为目前找到的最小窗口
        if target_count == 0 and temp < min_window_len:
            min_window = [window_start, window_end]
            exists = True
            min_window_len = temp

        # 向右移动窗口起点，直到某个待搜索字符离开窗口
        while target_count == 0 and window_start < window_end:
            cur = search_str[window_start]
            window_start += 1
            if cur in char_dict:
                char_dict[cur] += 1
                if char_dict[cur] > 0:
                    break
        temp = window_end - window_start + 1

        # 检查窗口是否为目前找到的最小窗口
        if temp < min_window_len and target_count == 0:
            min_window = [window_start - 1, window_end]
            min_window_len = temp
        target_count = 1

    if exists:
        return search_str[min_window[0] : min_window[1]]
    else:
        return ""
