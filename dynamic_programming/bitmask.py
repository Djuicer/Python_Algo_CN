"""

这是人员任务分配问题的 Python 实现。
这里使用位掩码（Bitmasking）和动态规划（DP）求解。

问题：
现有 N 个任务和 M 个人。M 个人中的每个人只能完成其中的某些任务。
此外，一个人只能完成一个任务，一个任务也只能由一个人完成。
求任务分配方式的总数。
"""

from collections import defaultdict


class AssignmentUsingBitmask:
    def __init__(self, task_performed, total) -> None:
        self.total_tasks = total  # 任务总数 (N)

        # DP 表的维度为 (2^M)*N
        # 初始时所有值都设为 -1
        self.dp = [
            [-1 for i in range(total + 1)] for j in range(2 ** len(task_performed))
        ]

        self.task = defaultdict(list)  # 存储每个任务对应的人员列表

        # final_mask 通过将所有位设为 1，检查是否已包含所有人员
        self.final_mask = (1 << len(task_performed)) - 1

    def count_ways_until(self, mask, task_no):
        # 如果 mask == self.finalmask，表示所有人员都已分配任务，返回 1
        if mask == self.final_mask:
            return 1

        # 如果仍有人未获得任务且没有更多可用任务，则返回 0
        if task_no > self.total_tasks:
            return 0

        # 如果该情况已经计算过
        if self.dp[mask][task_no] != -1:
            return self.dp[mask][task_no]

        # 分配方案中不采用当前任务时的方式数
        total_ways_until = self.count_ways_until(mask, task_no + 1)

        # 现在将任务逐一分配给所有可能的人员，并递归分配剩余任务
        if task_no in self.task:
            for p in self.task[task_no]:
                # 如果 p 已经分配了任务
                if mask & (1 << p):
                    continue

                # 将当前任务分配给 p 并更改 mask 值，然后使用新 mask 值递归分配任务
                total_ways_until += self.count_ways_until(mask | (1 << p), task_no + 1)

        # 保存该值
        self.dp[mask][task_no] = total_ways_until

        return self.dp[mask][task_no]

    def count_no_of_ways(self, task_performed):
        # 存储每个任务对应的人员列表
        for i in range(len(task_performed)):
            for j in task_performed[i]:
                self.task[j].append(i)

        # 调用函数填充 DP 表，最终答案存储在 dp[0][1] 中
        return self.count_ways_until(0, 1)


if __name__ == "__main__":
    total_tasks = 5  # 任务总数（N 的值）

    # M 个人可以完成的任务列表
    task_performed = [[1, 3, 4], [1, 2, 5], [3, 4]]
    print(
        AssignmentUsingBitmask(task_performed, total_tasks).count_no_of_ways(
            task_performed
        )
    )
    """
    对于此特定示例，任务分配方式如下：
    (1,2,3), (1,2,4), (1,5,3), (1,5,4), (3,1,4),
    (3,2,4), (3,5,4), (4,1,3), (4,2,3), (4,5,3)
    总计 10 种
    """
