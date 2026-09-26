def job_sequencing_with_deadlines(jobs: list) -> list:
    """
    求在给定时间范围内执行作业可获得的最大收益。

    参数：
        jobs [list]: 由 (job_id, deadline, profit) 元组组成的列表

    返回：
        max_profit [int]: 在给定时间范围内执行作业可获得的最大收益

    示例：
    >>> job_sequencing_with_deadlines(
    ... [(1, 4, 20), (2, 1, 10), (3, 1, 40), (4, 1, 30)])
    [2, 60]
    >>> job_sequencing_with_deadlines(
    ... [(1, 2, 100), (2, 1, 19), (3, 2, 27), (4, 1, 25), (5, 1, 15)])
    [2, 127]
    """

    # 按收益降序排列作业
    jobs = sorted(jobs, key=lambda value: value[2], reverse=True)

    # 创建长度等于最大截止期限的列表，并用 -1 初始化
    max_deadline = max(jobs, key=lambda value: value[1])[1]
    time_slots = [-1] * max_deadline

    # 求最大收益和作业数量
    count = 0
    max_profit = 0
    for job in jobs:
        # 为该作业寻找空闲时间段（注意从最后一个可能的时间段开始）
        for i in range(job[1] - 1, -1, -1):
            if time_slots[i] == -1:
                time_slots[i] = job[0]
                count += 1
                max_profit += job[2]
                break
    return [count, max_profit]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
