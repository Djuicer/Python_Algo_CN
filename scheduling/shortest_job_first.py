"""
最短剩余作业优先。
请注意到达时间和执行时间，输入各时间时使用空格分隔。
"""

from __future__ import annotations

import pandas as pd


def calculate_waitingtime(
    arrival_time: list[int], burst_time: list[int], no_of_processes: int
) -> list[int]:
    """
    计算各进程的等待时间。
    返回：等待时间列表。
    >>> calculate_waitingtime([1,2,3,4],[3,3,5,1],4)
    [0, 3, 5, 0]
    >>> calculate_waitingtime([1,2,3],[2,5,1],3)
    [0, 2, 0]
    >>> calculate_waitingtime([2,3],[5,1],2)
    [1, 0]
    """
    remaining_time = [0] * no_of_processes
    waiting_time = [0] * no_of_processes
    # 将执行时间复制到 remaining_time[]
    for i in range(no_of_processes):
        remaining_time[i] = burst_time[i]

    complete = 0
    increment_time = 0
    minm = 999999999
    short = 0
    check = False

    # 持续处理，直至所有进程完成
    while complete != no_of_processes:
        for j in range(no_of_processes):
            if (
                arrival_time[j] <= increment_time
                and remaining_time[j] > 0
                and remaining_time[j] < minm
            ):
                minm = remaining_time[j]
                short = j
                check = True

        if not check:
            increment_time += 1
            continue
        remaining_time[short] -= 1

        minm = remaining_time[short]
        if minm == 0:
            minm = 999999999

        if remaining_time[short] == 0:
            complete += 1
            check = False

            # 求当前进程的完成时间
            finish_time = increment_time + 1

            # 计算等待时间
            finar = finish_time - arrival_time[short]
            waiting_time[short] = finar - burst_time[short]

            waiting_time[short] = max(waiting_time[short], 0)

        # 增加时间
        increment_time += 1
    return waiting_time


def calculate_turnaroundtime(
    burst_time: list[int], no_of_processes: int, waiting_time: list[int]
) -> list[int]:
    """
    计算各进程的周转时间。
    返回：周转时间列表。
    >>> calculate_turnaroundtime([3,3,5,1], 4, [0,3,5,0])
    [3, 6, 10, 1]
    >>> calculate_turnaroundtime([3,3], 2, [0,3])
    [3, 6]
    >>> calculate_turnaroundtime([8,10,1], 3, [1,0,3])
    [9, 10, 4]
    """
    turn_around_time = [0] * no_of_processes
    for i in range(no_of_processes):
        turn_around_time[i] = burst_time[i] + waiting_time[i]
    return turn_around_time


def calculate_average_times(
    waiting_time: list[int], turn_around_time: list[int], no_of_processes: int
) -> None:
    """
    计算等待时间和周转时间的平均值。
    输出：平均等待时间和平均周转时间。
    >>> calculate_average_times([0,3,5,0],[3,6,10,1],4)
    Average waiting time = 2.00000
    Average turn around time = 5.0
    >>> calculate_average_times([2,3],[3,6],2)
    Average waiting time = 2.50000
    Average turn around time = 4.5
    >>> calculate_average_times([10,4,3],[2,7,6],3)
    Average waiting time = 5.66667
    Average turn around time = 5.0
    """
    total_waiting_time = 0
    total_turn_around_time = 0
    for i in range(no_of_processes):
        total_waiting_time = total_waiting_time + waiting_time[i]
        total_turn_around_time = total_turn_around_time + turn_around_time[i]
    print(f"Average waiting time = {total_waiting_time / no_of_processes:.5f}")
    print("Average turn around time =", total_turn_around_time / no_of_processes)


if __name__ == "__main__":
    print("Enter how many process you want to analyze")
    no_of_processes = int(input())
    burst_time = [0] * no_of_processes
    arrival_time = [0] * no_of_processes
    processes = list(range(1, no_of_processes + 1))

    for i in range(no_of_processes):
        print("Enter the arrival time and burst time for process:--" + str(i + 1))
        arrival_time[i], burst_time[i] = map(int, input().split())

    waiting_time = calculate_waitingtime(arrival_time, burst_time, no_of_processes)

    bt = burst_time
    n = no_of_processes
    wt = waiting_time
    turn_around_time = calculate_turnaroundtime(bt, n, wt)

    calculate_average_times(waiting_time, turn_around_time, no_of_processes)

    fcfs = pd.DataFrame(
        list(zip(processes, burst_time, arrival_time, waiting_time, turn_around_time)),
        columns=[
            "Process",
            "BurstTime",
            "ArrivalTime",
            "WaitingTime",
            "TurnAroundTime",
        ],
    )

    # 输出数据帧
    pd.set_option("display.max_rows", fcfs.shape[0] + 1)
    print(fcfs)
