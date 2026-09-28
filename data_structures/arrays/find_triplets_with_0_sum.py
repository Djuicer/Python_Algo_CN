from itertools import combinations


def find_triplets_with_0_sum(nums: list[int]) -> list[list[int]]:
    """
    给定一个整数列表，返回 元素，b，c such 该 + b + c = 0。
    参数：
        nums: 列表 的 整数
    返回值：
        列表 的 列表 的 整数 其中 和(each_list) == 0
    示例：
        >>> find_triplets_with_0_sum([-1, 0, 1, 2, -1, -4])
        [[-1, -1, 2], [-1, 0, 1]]
        >>> find_triplets_with_0_sum([])
        []
        >>> find_triplets_with_0_sum([0, 0, 0])
        [[0, 0, 0]]
        >>> find_triplets_with_0_sum([1, 2, 3, 0, -1, -2, -3])
        [[-3, 0, 3], [-3, 1, 2], [-2, -1, 3], [-2, 0, 2], [-1, 0, 1]]
    """
    return [
        list(x)
        for x in sorted({abc for abc in combinations(sorted(nums), 3) if not sum(abc)})
    ]


def find_triplets_with_0_sum_hashing(arr: list[int]) -> list[list[int]]:
    """
    函数 用于 finding triplets 带有 给定 和 在 该数组 使用哈希。

    给定一个整数列表，返回 元素，b，c such 该 + b + c = 0。

    参数：
        nums: 列表 的 整数
    返回值：
        列表 的 列表 的 整数 其中 和(each_list) == 0
    示例：
        >>> find_triplets_with_0_sum_hashing([-1, 0, 1, 2, -1, -4])
        [[-1, 0, 1], [-1, -1, 2]]
        >>> find_triplets_with_0_sum_hashing([])
        []
        >>> find_triplets_with_0_sum_hashing([0, 0, 0])
        [[0, 0, 0]]
        >>> find_triplets_with_0_sum_hashing([1, 2, 3, 0, -1, -2, -3])
        [[-1, 0, 1], [-3, 1, 2], [-2, 0, 2], [-2, -1, 3], [-3, 0, 3]]

    时间复杂度: O(N^2)
    辅助空间: O(N)

    """
    target_sum = 0

    # 初始化 最终 输出 数组 带有 blank。
    output_arr = []

    # 设置 初始 元素 作为 arr[i]。
    for index, item in enumerate(arr[:-2]):
        # 到 存储 第二个 元素 该 可以 complement 最终 和。
        set_initialize = set()

        # 当前 和 需要 用于 reaching 目标和
        current_sum = target_sum - item

        # 遍历 subarray arr[i+1:]。
        for other_item in arr[index + 1 :]:
            # 所需 值 用于 第二个 元素
            required_value = current_sum - other_item

            # Verify 如果 所需 值 存在 在 集合。
            if required_value in set_initialize:
                # finding triplet 元素 combination。
                combination_array = sorted([item, other_item, required_value])
                if combination_array not in output_arr:
                    output_arr.append(combination_array)

            # Include 当前元素 在 集合
            # 用于 subsequent complement verification。
            set_initialize.add(other_item)

    # 返回所有 triplet combinations。
    return output_arr


def find_triplets_with_0_sum_two_pointers(nums: list[int]) -> list[list[int]]:
    """
    查找所有 唯一 triplets 在 该数组 其 gives 和 的 zero
    使用双指针技术。

    参数：
        nums: 列表 的 整数
    返回值：
        列表 的 列表 的 整数 其中 和(each_list) == 0

    示例：
        >>> find_triplets_with_0_sum_two_pointers([-1, 0, 1, 2, -1, -4])
        [[-1, -1, 2], [-1, 0, 1]]
        >>> find_triplets_with_0_sum_two_pointers([])
        []
        >>> find_triplets_with_0_sum_two_pointers([0, 0, 0, 0])
        [[0, 0, 0]]

    时间复杂度: O(N^2)
    辅助空间: O(1) (不包括 输出)
    """
    nums.sort()
    result = []
    n = len(nums)

    for i in range(n - 2):
        if i > 0 and nums[i] == nums[i - 1]:
            continue

        left, right = i + 1, n - 1

        while left < right:
            total = nums[i] + nums[left] + nums[right]

            if total == 0:
                result.append([nums[i], nums[left], nums[right]])
                left += 1
                right -= 1

                while left < right and nums[left] == nums[left - 1]:
                    left += 1
                while left < right and nums[right] == nums[right + 1]:
                    right -= 1

            elif total < 0:
                left += 1
            else:
                right -= 1

    return result


if __name__ == "__main__":
    from doctest import testmod

    testmod()
