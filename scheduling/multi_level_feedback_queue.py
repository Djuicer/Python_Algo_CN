from collections import deque


class Process:
    def __init__(self, process_name: str, arrival_time: int, burst_time: int) -> None:
        self.process_name = process_name  # 进程名称
        self.arrival_time = arrival_time  # 进程到达时间
        # 已完成进程的完成时间或上次中断时间
        self.stop_time = arrival_time
        self.burst_time = burst_time  # 剩余执行时间
        self.waiting_time = 0  # 进程在就绪队列中的总等待时间
        self.turnaround_time = 0  # 从到达至完成所用的时间


class MLFQ:
    """
    多级反馈队列（Multi Level Feedback Queue，MLFQ）
    https://en.wikipedia.org/wiki/Multilevel_feedback_queue
    MLFQ 包含多个优先级不同的队列。
    在此 MLFQ 中，从第一个队列 Queue(0) 到倒数第二个队列 Queue(N-2) 使用
    轮转调度算法，最后一个队列 Queue(N-1) 使用先来先服务算法。
    """

    def __init__(
        self,
        number_of_queues: int,
        time_slices: list[int],
        queue: deque[Process],
        current_time: int,
    ) -> None:
        # MLFQ 的队列总数
        self.number_of_queues = number_of_queues
        # 采用轮转调度的各队列时间片
        self.time_slices = time_slices
        # 未完成进程位于此就绪队列
        self.ready_queue = queue
        # 当前时间
        self.current_time = current_time
        # 已完成进程位于此顺序队列
        self.finish_queue: deque[Process] = deque()

    def calculate_sequence_of_finish_queue(self) -> list[str]:
        """
        返回进程完成顺序。
        >>> P1 = Process("P1", 0, 53)
        >>> P2 = Process("P2", 0, 17)
        >>> P3 = Process("P3", 0, 68)
        >>> P4 = Process("P4", 0, 24)
        >>> mlfq = MLFQ(3, [17, 25], deque([P1, P2, P3, P4]), 0)
        >>> _ = mlfq.multi_level_feedback_queue()
        >>> mlfq.calculate_sequence_of_finish_queue()
        ['P2', 'P4', 'P1', 'P3']
        """
        sequence = []
        for i in range(len(self.finish_queue)):
            sequence.append(self.finish_queue[i].process_name)
        return sequence

    def calculate_waiting_time(self, queue: list[Process]) -> list[int]:
        """
        计算进程的等待时间。
        >>> P1 = Process("P1", 0, 53)
        >>> P2 = Process("P2", 0, 17)
        >>> P3 = Process("P3", 0, 68)
        >>> P4 = Process("P4", 0, 24)
        >>> mlfq = MLFQ(3, [17, 25], deque([P1, P2, P3, P4]), 0)
        >>> _ = mlfq.multi_level_feedback_queue()
        >>> mlfq.calculate_waiting_time([P1, P2, P3, P4])
        [83, 17, 94, 101]
        """
        waiting_times = []
        for i in range(len(queue)):
            waiting_times.append(queue[i].waiting_time)
        return waiting_times

    def calculate_turnaround_time(self, queue: list[Process]) -> list[int]:
        """
        计算进程的周转时间。
        >>> P1 = Process("P1", 0, 53)
        >>> P2 = Process("P2", 0, 17)
        >>> P3 = Process("P3", 0, 68)
        >>> P4 = Process("P4", 0, 24)
        >>> mlfq = MLFQ(3, [17, 25], deque([P1, P2, P3, P4]), 0)
        >>> _ = mlfq.multi_level_feedback_queue()
        >>> mlfq.calculate_turnaround_time([P1, P2, P3, P4])
        [136, 34, 162, 125]
        """
        turnaround_times = []
        for i in range(len(queue)):
            turnaround_times.append(queue[i].turnaround_time)
        return turnaround_times

    def calculate_completion_time(self, queue: list[Process]) -> list[int]:
        """
        计算进程的完成时间。
        >>> P1 = Process("P1", 0, 53)
        >>> P2 = Process("P2", 0, 17)
        >>> P3 = Process("P3", 0, 68)
        >>> P4 = Process("P4", 0, 24)
        >>> mlfq = MLFQ(3, [17, 25], deque([P1, P2, P3, P4]), 0)
        >>> _ = mlfq.multi_level_feedback_queue()
        >>> mlfq.calculate_completion_time([P1, P2, P3, P4])
        [136, 34, 162, 125]
        """
        completion_times = []
        for i in range(len(queue)):
            completion_times.append(queue[i].stop_time)
        return completion_times

    def calculate_remaining_burst_time_of_processes(
        self, queue: deque[Process]
    ) -> list[int]:
        """
        计算进程的剩余执行时间。
        >>> P1 = Process("P1", 0, 53)
        >>> P2 = Process("P2", 0, 17)
        >>> P3 = Process("P3", 0, 68)
        >>> P4 = Process("P4", 0, 24)
        >>> mlfq = MLFQ(3, [17, 25], deque([P1, P2, P3, P4]), 0)
        >>> finish_queue, ready_queue = mlfq.round_robin(deque([P1, P2, P3, P4]), 17)
        >>> mlfq.calculate_remaining_burst_time_of_processes(mlfq.finish_queue)
        [0]
        >>> mlfq.calculate_remaining_burst_time_of_processes(ready_queue)
        [36, 51, 7]
        >>> finish_queue, ready_queue = mlfq.round_robin(ready_queue, 25)
        >>> mlfq.calculate_remaining_burst_time_of_processes(mlfq.finish_queue)
        [0, 0]
        >>> mlfq.calculate_remaining_burst_time_of_processes(ready_queue)
        [11, 26]
        """
        return [q.burst_time for q in queue]

    def update_waiting_time(self, process: Process) -> int:
        """
        更新未完成进程的等待时间。
        >>> P1 = Process("P1", 0, 53)
        >>> P2 = Process("P2", 0, 17)
        >>> P3 = Process("P3", 0, 68)
        >>> P4 = Process("P4", 0, 24)
        >>> mlfq = MLFQ(3, [17, 25], deque([P1, P2, P3, P4]), 0)
        >>> mlfq.current_time = 10
        >>> P1.stop_time = 5
        >>> mlfq.update_waiting_time(P1)
        5
        """
        process.waiting_time += self.current_time - process.stop_time
        return process.waiting_time

    def first_come_first_served(self, ready_queue: deque[Process]) -> deque[Process]:
        """
        先来先服务（First Come, First Served，FCFS）
        FCFS 应用于 MLFQ 的最后一个队列，先到达的进程先完成。
        >>> P1 = Process("P1", 0, 53)
        >>> P2 = Process("P2", 0, 17)
        >>> P3 = Process("P3", 0, 68)
        >>> P4 = Process("P4", 0, 24)
        >>> mlfq = MLFQ(3, [17, 25], deque([P1, P2, P3, P4]), 0)
        >>> _ = mlfq.first_come_first_served(mlfq.ready_queue)
        >>> mlfq.calculate_sequence_of_finish_queue()
        ['P1', 'P2', 'P3', 'P4']
        """
        finished: deque[Process] = deque()  # 已完成进程的顺序双端队列
        while len(ready_queue) != 0:
            cp = ready_queue.popleft()  # 当前进程

            # 若进程到达时间晚于当前时间，则更新当前时间
            if self.current_time < cp.arrival_time:
                self.current_time += cp.arrival_time

            # 更新当前进程的等待时间
            self.update_waiting_time(cp)
            # 更新当前时间
            self.current_time += cp.burst_time
            # 完成进程，并将其执行时间设为 0
            cp.burst_time = 0
            # 进程已完成，设置其周转时间
            cp.turnaround_time = self.current_time - cp.arrival_time
            # 设置完成时间
            cp.stop_time = self.current_time
            # 将进程加入已完成队列
            finished.append(cp)

        self.finish_queue.extend(finished)  # 将已完成进程加入 finish_queue
        # FCFS 会完成所有剩余进程
        return finished

    def round_robin(
        self, ready_queue: deque[Process], time_slice: int
    ) -> tuple[deque[Process], deque[Process]]:
        """
        轮转调度（Round Robin，RR）
        RR 应用于 MLFQ 中除最后一个队列外的所有队列。
        所有进程使用 CPU 的时间均不能超过 time_slice；若进程用满 time_slice，
        则返回就绪队列。
        >>> P1 = Process("P1", 0, 53)
        >>> P2 = Process("P2", 0, 17)
        >>> P3 = Process("P3", 0, 68)
        >>> P4 = Process("P4", 0, 24)
        >>> mlfq = MLFQ(3, [17, 25], deque([P1, P2, P3, P4]), 0)
        >>> finish_queue, ready_queue = mlfq.round_robin(mlfq.ready_queue, 17)
        >>> mlfq.calculate_sequence_of_finish_queue()
        ['P2']
        """
        finished: deque[Process] = deque()  # 已终止进程的顺序双端队列
        # 只执行一轮，未完成进程将返回队列
        for _ in range(len(ready_queue)):
            cp = ready_queue.popleft()  # 当前进程

            # 若进程到达时间晚于当前时间，则更新当前时间
            if self.current_time < cp.arrival_time:
                self.current_time += cp.arrival_time

            # 更新未完成进程的等待时间
            self.update_waiting_time(cp)
            # 若进程执行时间大于时间片
            if cp.burst_time > time_slice:
                # 仅使用一个时间片的 CPU
                self.current_time += time_slice
                # 更新剩余执行时间
                cp.burst_time -= time_slice
                # 更新结束时间
                cp.stop_time = self.current_time
                # 进程尚未完成，将其放到队尾
                ready_queue.append(cp)
            else:
                # 使用 CPU 完成剩余执行时间
                self.current_time += cp.burst_time
                # 进程已完成，将执行时间设为 0
                cp.burst_time = 0
                # 设置完成时间
                cp.stop_time = self.current_time
                # 进程已完成，更新其周转时间
                cp.turnaround_time = self.current_time - cp.arrival_time
                # 将进程加入已完成队列
                finished.append(cp)

        self.finish_queue.extend(finished)  # 将已完成进程加入 finish_queue
        # 返回已完成进程队列和剩余进程队列
        return finished, ready_queue

    def multi_level_feedback_queue(self) -> deque[Process]:
        """
        多级反馈队列（Multi Level Feedback Queue，MLFQ）
        >>> P1 = Process("P1", 0, 53)
        >>> P2 = Process("P2", 0, 17)
        >>> P3 = Process("P3", 0, 68)
        >>> P4 = Process("P4", 0, 24)
        >>> mlfq = MLFQ(3, [17, 25], deque([P1, P2, P3, P4]), 0)
        >>> finish_queue = mlfq.multi_level_feedback_queue()
        >>> mlfq.calculate_sequence_of_finish_queue()
        ['P2', 'P4', 'P1', 'P3']
        """

        # 除最后一个队列外，所有队列均采用 round_robin 算法
        for i in range(self.number_of_queues - 1):
            _finished, self.ready_queue = self.round_robin(
                self.ready_queue, self.time_slices[i]
            )
        # 最后一个队列采用 first_come_first_served 算法
        self.first_come_first_served(self.ready_queue)

        return self.finish_queue


if __name__ == "__main__":
    import doctest

    P1 = Process("P1", 0, 53)
    P2 = Process("P2", 0, 17)
    P3 = Process("P3", 0, 68)
    P4 = Process("P4", 0, 24)
    number_of_queues = 3
    time_slices = [17, 25]
    queue = deque([P1, P2, P3, P4])

    if len(time_slices) != number_of_queues - 1:
        raise SystemExit(0)

    doctest.testmod(extraglobs={"queue": deque([P1, P2, P3, P4])})

    P1 = Process("P1", 0, 53)
    P2 = Process("P2", 0, 17)
    P3 = Process("P3", 0, 68)
    P4 = Process("P4", 0, 24)
    number_of_queues = 3
    time_slices = [17, 25]
    queue = deque([P1, P2, P3, P4])
    mlfq = MLFQ(number_of_queues, time_slices, queue, 0)
    finish_queue = mlfq.multi_level_feedback_queue()

    # 输出进程（P1、P2、P3、P4）的总等待时间
    print(
        f"waiting time:\
        \t\t\t{MLFQ.calculate_waiting_time(mlfq, [P1, P2, P3, P4])}"
    )
    # 输出进程（P1、P2、P3、P4）的完成时间
    print(
        f"completion time:\
        \t\t{MLFQ.calculate_completion_time(mlfq, [P1, P2, P3, P4])}"
    )
    # 输出进程（P1、P2、P3、P4）的总周转时间
    print(
        f"turnaround time:\
        \t\t{MLFQ.calculate_turnaround_time(mlfq, [P1, P2, P3, P4])}"
    )
    # 输出进程完成顺序
    print(
        f"sequence of finished processes:\
        {mlfq.calculate_sequence_of_finish_queue()}"
    )
