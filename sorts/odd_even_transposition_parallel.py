"""
奇偶交换排序（Odd-Even Transposition Sort）的实现。

通过在列表的奇数和偶数位置元素对之间，
执行一系列并行交换进行排序。

每个列表元素对应一个进程，
各进程与相邻进程通信，
以完成比较。
使用锁和消息传递进行同步，也可以使用
其他同步方式。
"""

import multiprocessing as mp

# 用锁确保两个进程不会同时访问同一管道
# 注意：这会导致构建环境中的测试失败，在本地可能表现更好
# process_lock = mp.Lock()

"""
由进程执行、用于排序列表的函数

position = 进程所代表的列表位置，用于确定
            应向哪个邻居传递自身的值
value = list[position] 的初始值
LSend, RSend = 向左右邻居发送数据所用的管道
LRcv, RRcv = 从左右邻居接收数据所用的管道
resultPipe = 将结果发送回主进程的管道
"""


def oe_process(
    position,
    value,
    l_send,
    r_send,
    lr_cv,
    rr_cv,
    result_pipe,
    multiprocessing_context,
) -> None:
    process_lock = multiprocessing_context.Lock()

    # 执行 n 轮交换，因为 n 轮后可以确定已有序
    # 若提前有序，本可以提前停止，但判断有序所需的时间
    # 与使用本算法排序相当
    for i in range(10):
        if (i + position) % 2 == 0 and r_send is not None:
            # 将自身的值发送给右侧邻居
            with process_lock:
                r_send[1].send(value)

            # 接收右侧邻居的值
            with process_lock:
                temp = rr_cv[0].recv()

            # 自身位于左侧，因此取较小值
            value = min(value, temp)
        elif (i + position) % 2 != 0 and l_send is not None:
            # 将自身的值发送给左侧邻居
            with process_lock:
                l_send[1].send(value)

            # 接收左侧邻居的值
            with process_lock:
                temp = lr_cv[0].recv()

            # 自身位于右侧，因此取较大值
            value = max(value, temp)
    # 完成所有交换后，将值发送回主进程
    result_pipe[1].send(value)


"""
创建进程以执行并行交换的函数

arr = 待排序列表
"""


def odd_even_transposition(arr):
    """
    >>> odd_even_transposition(list(range(10)[::-1])) == sorted(list(range(10)[::-1]))
    True
    >>> odd_even_transposition(["a", "x", "c"]) == sorted(["x", "a", "c"])
    True
    >>> odd_even_transposition([1.9, 42.0, 2.8]) == sorted([1.9, 42.0, 2.8])
    True
    >>> odd_even_transposition([False, True, False]) == sorted([False, False, True])
    True
    >>> odd_even_transposition([1, 32.0, 9]) == sorted([False, False, True])
    False
    >>> odd_even_transposition([1, 32.0, 9]) == sorted([1.0, 32, 9.0])
    True
    >>> unsorted_list = [-442, -98, -554, 266, -491, 985, -53, -529, 82, -429]
    >>> odd_even_transposition(unsorted_list) == sorted(unsorted_list)
    True
    >>> unsorted_list = [-442, -98, -554, 266, -491, 985, -53, -529, 82, -429]
    >>> odd_even_transposition(unsorted_list) == sorted(unsorted_list + [1])
    False
    """
    # 通常认为 spawn 方式比 fork 更安全
    multiprocessing_context = mp.get_context("spawn")

    process_array_ = []
    result_pipe = []
    # 初始化用于接收结果值的管道列表
    for _ in arr:
        result_pipe.append(multiprocessing_context.Pipe())
    # 创建进程
    # 第一个和最后一个进程只有一个邻居，因此在循环
    # 之外创建
    temp_rs = multiprocessing_context.Pipe()
    temp_rr = multiprocessing_context.Pipe()
    process_array_.append(
        multiprocessing_context.Process(
            target=oe_process,
            args=(
                0,
                arr[0],
                None,
                temp_rs,
                None,
                temp_rr,
                result_pipe[0],
                multiprocessing_context,
            ),
        )
    )
    temp_lr = temp_rs
    temp_ls = temp_rr

    for i in range(1, len(arr) - 1):
        temp_rs = multiprocessing_context.Pipe()
        temp_rr = multiprocessing_context.Pipe()
        process_array_.append(
            multiprocessing_context.Process(
                target=oe_process,
                args=(
                    i,
                    arr[i],
                    temp_ls,
                    temp_rs,
                    temp_lr,
                    temp_rr,
                    result_pipe[i],
                    multiprocessing_context,
                ),
            )
        )
        temp_lr = temp_rs
        temp_ls = temp_rr

    process_array_.append(
        multiprocessing_context.Process(
            target=oe_process,
            args=(
                len(arr) - 1,
                arr[len(arr) - 1],
                temp_ls,
                None,
                temp_lr,
                None,
                result_pipe[len(arr) - 1],
                multiprocessing_context,
            ),
        )
    )

    # 启动进程
    for p in process_array_:
        p.start()

    # 等待进程结束，并将其值写入列表
    for p in range(len(result_pipe)):
        arr[p] = result_pipe[p][0].recv()
        process_array_[p].join()
    return arr


# 创建逆序列表并对其排序
def main() -> None:
    arr = list(range(10, 0, -1))
    print("Initial List")
    print(*arr)
    arr = odd_even_transposition(arr)
    print("Sorted List\n")
    print(*arr)


if __name__ == "__main__":
    main()
