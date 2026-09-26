"""
测试用例：
Do you want to enter your denominations ? (Y/N) :N
Enter the change you want to make in Indian Currency: 987
Following is minimal  change for 987 :
500 100 100 100 100 50 20 10 5 2

Do you want to enter your denominations ? (Y/N) :Y
Enter number of denomination:10
1
5
10
20
50
100
200
500
1000
2000
Enter the change you want to make: 18745
Following is minimal  change for 18745 :
2000 2000 2000 2000 2000 2000 2000 2000 2000 500 200 20 20 5

Do you want to enter your denominations ? (Y/N) :N
Enter the change you want to make: 0
The total value cannot be zero or negative.
Do you want to enter your denominations ? (Y/N) :N
Enter the change you want to make: -98
The total value cannot be zero or negative.

Do you want to enter your denominations ? (Y/N) :Y
Enter number of denomination:5
1
5
100
500
1000
Enter the change you want to make: 456
Following is minimal   change for 456 :
100 100 100 100 5 5 5 5 5 5 5 5 5 5 5 1
"""


def find_minimum_change(denominations: list[int], value: str) -> list[int]:
    """
    根据给定面额和金额，求最少硬币找零方案
    >>> find_minimum_change([1, 5, 10, 20, 50, 100, 200, 500, 1000,2000], 18745)
    [2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 500, 200, 20, 20, 5]
    >>> find_minimum_change([1, 2, 5, 10, 20, 50, 100, 500, 2000], 987)
    [500, 100, 100, 100, 100, 50, 20, 10, 5, 2]
    >>> find_minimum_change([1, 2, 5, 10, 20, 50, 100, 500, 2000], 0)
    []
    >>> find_minimum_change([1, 2, 5, 10, 20, 50, 100, 500, 2000], -98)
    []
    >>> find_minimum_change([1, 5, 100, 500, 1000], 456)
    [100, 100, 100, 100, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 1]
    """
    total_value = int(value)

    # 初始化结果
    answer = []

    # 遍历所有面额
    for denomination in reversed(denominations):
        # 寻找可用面额
        while int(total_value) >= int(denomination):
            total_value -= int(denomination)
            answer.append(denomination)  # 追加到 "answers" 数组

    return answer


# 主程序代码
if __name__ == "__main__":
    denominations = []
    value = "0"

    if (
        input("Do you want to enter your denominations ? (yY/n): ").strip().lower()
        == "y"
    ):
        n = int(input("Enter the number of denominations you want to add: ").strip())

        for i in range(n):
            denominations.append(int(input(f"Denomination {i}: ").strip()))
        value = input("Enter the change you want to make in Indian Currency: ").strip()
    else:
        # 用户未输入面额时，使用印度货币的所有面额
        denominations = [1, 2, 5, 10, 20, 50, 100, 500, 2000]
        value = input("Enter the change you want to make: ").strip()

    if int(value) == 0 or int(value) < 0:
        print("The total value cannot be zero or negative.")

    else:
        print(f"Following is minimal change for {value}: ")
        answer = find_minimum_change(denominations, value)
        # 输出结果
        for i in range(len(answer)):
            print(answer[i], end=" ")
