# 先来先服务（First Come First Served，FCFS）调度算法的实现
# 本算法只关心进程到达顺序，不考虑其执行时长
# https://en.wikipedia.org/wiki/Scheduling_(computing)#First_come,_first_served
from __future__ import annotations


def calculate_waiting_times(duration_times: list[int]) -> list[int]:
    """
    计算一组具有指定执行时长的进程的等待时间。
        返回：各进程的等待时间。
    >>> calculate_waiting_times([5, 10, 15])
    [0, 5, 15]
    >>> calculate_waiting_times([1, 2, 3, 4, 5])
    [0, 1, 3, 6, 10]
    >>> calculate_waiting_times([10, 3])
    [0, 10]
    """
    waiting_times = [0] * len(duration_times)
    for i in range(1, len(duration_times)):
        waiting_times[i] = duration_times[i - 1] + waiting_times[i - 1]
    return waiting_times


def calculate_turnaround_times(
    duration_times: list[int], waiting_times: list[int]
) -> list[int]:
    """
    计算一组进程的周转时间。
        返回：完成时间与到达时间之差，实际上等于 waiting_time + duration_time。
    >>> calculate_turnaround_times([5, 10, 15], [0, 5, 15])
    [5, 15, 30]
    >>> calculate_turnaround_times([1, 2, 3, 4, 5], [0, 1, 3, 6, 10])
    [1, 3, 6, 10, 15]
    >>> calculate_turnaround_times([10, 3], [0, 10])
    [10, 13]
    """
    return [
        duration_time + waiting_times[i]
        for i, duration_time in enumerate(duration_times)
    ]


def calculate_average_turnaround_time(turnaround_times: list[int]) -> float:
    """
    计算平均周转时间。
        返回：周转时间的平均值。
    >>> calculate_average_turnaround_time([0, 5, 16])
    7.0
    >>> calculate_average_turnaround_time([1, 5, 8, 12])
    6.5
    >>> calculate_average_turnaround_time([10, 24])
    17.0
    """
    return sum(turnaround_times) / len(turnaround_times)


def calculate_average_waiting_time(waiting_times: list[int]) -> float:
    """
    计算平均等待时间。
        返回：等待时间的平均值。
    >>> calculate_average_waiting_time([0, 5, 16])
    7.0
    >>> calculate_average_waiting_time([1, 5, 8, 12])
    6.5
    >>> calculate_average_waiting_time([10, 24])
    17.0
    """
    return sum(waiting_times) / len(waiting_times)


if __name__ == "__main__":
    # 进程 ID
    processes = [1, 2, 3]

    # 确保确实存在进程
    if len(processes) == 0:
        print("Zero amount of processes")
        raise SystemExit(0)

    # 所有进程的执行时长
    duration_times = [19, 8, 9]

    # 确保每个 ID 都能匹配一个执行时长
    if len(duration_times) != len(processes):
        print("Unable to match all id's with their duration time")
        raise SystemExit(0)

    # 获取等待时间和周转时间
    waiting_times = calculate_waiting_times(duration_times)
    turnaround_times = calculate_turnaround_times(duration_times, waiting_times)

    # 获取平均时间
    average_waiting_time = calculate_average_waiting_time(waiting_times)
    average_turnaround_time = calculate_average_turnaround_time(turnaround_times)

    # 输出所有结果
    print("Process ID\tDuration Time\tWaiting Time\tTurnaround Time")
    for i, process in enumerate(processes):
        print(
            f"{process}\t\t{duration_times[i]}\t\t{waiting_times[i]}\t\t"
            f"{turnaround_times[i]}"
        )
    print(f"Average waiting time = {average_waiting_time}")
    print(f"Average turn around time = {average_turnaround_time}")
