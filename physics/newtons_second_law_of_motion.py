r"""
说明：
    牛顿第二运动定律描述所受各力不平衡的物体。该定律指出，物体的加速度
    取决于所受合力和物体质量：加速度与合力成正比，与质量成反比。合力增大
    时加速度增大；质量增大时加速度减小。

来源：https://www.physicsclassroom.com/class/newtlaws/Lesson-3/Newton-s-Second-Law

公式：F_net = m • a

图示说明：

                    力不平衡
                        |
                        |
                        |
                        V
                    存在加速度
                        /\
                       /  \
                      /    \
                     /      \
                    /        \
                   /          \
                  /            \
    __________________      ____________________
   |  加速度与合力    |    |  加速度与物体     |
   |  成正比          |    |  质量成反比       |
   |                  |    |                   |
   |                  |    |                   |
   |__________________|    |____________________|

单位：1 Newton = 1 kg • meters/seconds^2

用法

输入：

    ______________ _____________________ ___________
   | 名称         | 单位                | 类型      |
   |--------------|---------------------|-----------|
   | mass         | in kgs              | float     |
   |--------------|---------------------|-----------|
   | acceleration | in meters/seconds^2 | float     |
   |______________|_____________________|___________|

输出：

    ______________ _______________________ ___________
   | 名称         | 单位                  | 类型      |
   |--------------|-----------------------|-----------|
   | force        | in Newtons            | float     |
   |______________|_______________________|___________|

"""


def newtons_second_law_of_motion(mass: float, acceleration: float) -> float:
    """
    根据 `mass` 和 `acceleration` 计算力。

    >>> newtons_second_law_of_motion(10, 10)
    100
    >>> newtons_second_law_of_motion(2.0, 1)
    2.0
    """
    force = 0.0
    try:
        force = mass * acceleration
    except Exception:
        return -0.0
    return force


if __name__ == "__main__":
    import doctest

    # 运行 doctest
    doctest.testmod()

    # 演示
    mass = 12.5
    acceleration = 10
    force = newtons_second_law_of_motion(mass, acceleration)
    print("The force is ", force, "N")
