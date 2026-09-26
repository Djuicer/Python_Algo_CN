"""
子集和问题给定一个非负整数集合及
数值 M，要求找出该集合中所有元素和
等于 M 的子集。

所选数字之和必须等于给定的 M，每个数字
只能使用一次。
"""


def generate_sum_of_subsets_solutions(nums: list[int], max_sum: int) -> list[list[int]]:
    """
    主函数。对于数值列表 'nums'，找出元素和
    等于 'max_sum' 的子集

    >>> generate_sum_of_subsets_solutions(nums=[3, 34, 4, 12, 5, 2], max_sum=9)
    [[3, 4, 2], [4, 5]]
    >>> generate_sum_of_subsets_solutions(nums=[3, 34, 4, 12, 5, 2], max_sum=3)
    [[3]]
    >>> generate_sum_of_subsets_solutions(nums=[3, 34, 4, 12, 5, 2], max_sum=1)
    []
    """

    result: list[list[int]] = []
    path: list[int] = []
    num_index = 0
    remaining_nums_sum = sum(nums)
    create_state_space_tree(nums, max_sum, num_index, path, result, remaining_nums_sum)
    return result


def create_state_space_tree(
    nums: list[int],
    max_sum: int,
    num_index: int,
    path: list[int],
    result: list[list[int]],
    remaining_nums_sum: int,
) -> None:
    """
    创建状态空间树，使用深度优先搜索（DFS）遍历各分支。
    满足下面两个条件中的任意一个时，
    终止该节点的分支扩展。
    此算法采用深度优先搜索，在节点无法继续
    扩展时回溯。

    >>> path = []
    >>> result = []
    >>> create_state_space_tree(
    ...     nums=[1],
    ...     max_sum=1,
    ...     num_index=0,
    ...     path=path,
    ...     result=result,
    ...     remaining_nums_sum=1)
    >>> path
    []
    >>> result
    [[1]]
    """

    if sum(path) > max_sum or (remaining_nums_sum + sum(path)) < max_sum:
        return
    if sum(path) == max_sum:
        result.append(path)
        return
    for index in range(num_index, len(nums)):
        create_state_space_tree(
            nums,
            max_sum,
            index + 1,
            [*path, nums[index]],
            result,
            remaining_nums_sum - nums[index],
        )


if __name__ == "__main__":
    import doctest

    doctest.testmod()
