"""简单混沌机的示例。"""

# 混沌机（K、t、m）
K = [0.33, 0.44, 0.55, 0.44, 0.33]
t = 3
m = 5

# 缓冲区空间（含参数空间）
buffer_space: list[float] = []
params_space: list[float] = []

# 机器时间
machine_time = 0


def push(seed) -> None:
    global buffer_space, params_space, machine_time

    # 选择全部动力系统
    for key, value in enumerate(buffer_space):
        # 演化参数
        e = float(seed / value)

        # 控制理论：轨道变化
        value = (buffer_space[(key + 1) % m] + e) % 1

        # 控制理论：轨迹变化
        r = (params_space[key] + e) % 1 + 3

        # 修改（转移函数）——跳跃
        buffer_space[key] = round(float(r * value * (1 - value)), 10)
        params_space[key] = r  # 保存到参数空间

    # 逻辑斯谛映射
    assert max(buffer_space) < 1
    assert max(params_space) < 4

    # 机器时间
    machine_time += 1


def pull():
    global buffer_space, params_space, machine_time

    # 选择动力系统（递增）
    key = machine_time % m

    # 演化（时间长度）
    for _ in range(t):
        # 变量（位置与参数）
        r = params_space[key]
        value = buffer_space[key]

        # 修改（转移函数）——流动
        buffer_space[key] = round(float(r * value * (1 - value)), 10)
        params_space[key] = (machine_time * 0.01 + r * 1.01) % 1 + 3

    # 选择混沌数据
    x = int(buffer_space[(key + 2) % m] * (10**10))
    y = int(buffer_space[(key - 2) % m] * (10**10))

    # 机器时间
    machine_time += 1

    # 伪随机数生成器（George Marsaglia 提出的 Xorshift）
    x ^= y >> 13
    y ^= x << 17
    x ^= y >> 5
    return x & 0xFFFFFFFF


def reset() -> None:
    global buffer_space, params_space, machine_time

    buffer_space = K
    params_space = [0] * m
    machine_time = 0


if __name__ == "__main__":
    # 初始化
    reset()

    # 推入数据（输入）
    import random

    message = random.sample(range(0xFFFFFFFF), 100)
    for chunk in message:
        push(chunk)

    # 用于控制循环
    inp = ""

    # 拉取数据（输出）
    while inp not in ("e", "E"):
        print(f"{format(pull(), '#04x')}")
        print(buffer_space)
        print(params_space)
        inp = input("(e)exit? ").strip()
