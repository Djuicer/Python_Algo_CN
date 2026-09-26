"""
非抢占式最短作业优先（Shortest Job First，SJF）。
选择执行时间最短的进程作为下一个执行对象。
https://www.guru99.com/shortest-job-first-sjf-scheduling.html
https://en.wikipedia.org/wiki/Shortest_job_next
"""

from __future__ import annotations

from statistics import mean


def calculate_waitingtime(
    arrival_time: list[int], burst_time: list[int], no_of_processes: int
) -> list[int]:
    """
    计算各进程的等待时间。

    返回：各进程的等待时间。
    >>> calculate_waitingtime([0,1,2], [10, 5, 8], 3)
    [0, 9, 13]
    >>> calculate_waitingtime([1,2,2,4], [4, 6, 3, 1], 4)
    [0, 7, 4, 1]
    >>> calculate_waitingtime([0,0,0], [12, 2, 10],3)
    [12, 0, 2]
    """

    waiting_time = [0] * no_of_processes
    remaining_time = [0] * no_of_processes

    # 将 remaining_time 初始化为 waiting_time

    for i in range(no_of_processes):
        remaining_time[i] = burst_time[i]
    ready_process: list[int] = []

    completed = 0
    total_time = 0

    # 当仍有进程未完成时，将已经到达且仍有剩余执行时间的进程放入
    # ready_process，并执行其中最短的进程 target_process

    while completed != no_of_processes:
        ready_process = []
        target_process = -1

        for i in range(no_of_processes):
            if (arrival_time[i] <= total_time) and (remaining_time[i] > 0):
                ready_process.append(i)

        if len(ready_process) > 0:
            target_process = ready_process[0]
            for i in ready_process:
                if remaining_time[i] < remaining_time[target_process]:
                    target_process = i
            total_time += burst_time[target_process]
            completed += 1
            remaining_time[target_process] = 0
            waiting_time[target_process] = (
                total_time - arrival_time[target_process] - burst_time[target_process]
            )
        else:
            total_time += 1

    return waiting_time


def calculate_turnaroundtime(
    burst_time: list[int], no_of_processes: int, waiting_time: list[int]
) -> list[int]:
    """
    计算各进程的周转时间。

    返回：各进程的周转时间。
    >>> calculate_turnaroundtime([0,1,2], 3, [0, 10, 15])
    [0, 11, 17]
    >>> calculate_turnaroundtime([1,2,2,4], 4, [1, 8, 5, 4])
    [2, 10, 7, 8]
    >>> calculate_turnaroundtime([0,0,0], 3, [12, 0, 2])
    [12, 0, 2]
    """

    turn_around_time = [0] * no_of_processes
    for i in range(no_of_processes):
        turn_around_time[i] = burst_time[i] + waiting_time[i]
    return turn_around_time


if __name__ == "__main__":
    print("[TEST CASE 01]")

    no_of_processes = 4
    burst_time = [2, 5, 3, 7]
    arrival_time = [0, 0, 0, 0]
    waiting_time = calculate_waitingtime(arrival_time, burst_time, no_of_processes)
    turn_around_time = calculate_turnaroundtime(
        burst_time, no_of_processes, waiting_time
    )

    # 输出结果
    print("PID\tBurst Time\tArrival Time\tWaiting Time\tTurnaround Time")
    for i, process_id in enumerate(list(range(1, 5))):
        print(
            f"{process_id}\t{burst_time[i]}\t\t\t{arrival_time[i]}\t\t\t\t"
            f"{waiting_time[i]}\t\t\t\t{turn_around_time[i]}"
        )
    print(f"\nAverage waiting time = {mean(waiting_time):.5f}")
    print(f"Average turnaround time = {mean(turn_around_time):.5f}")
