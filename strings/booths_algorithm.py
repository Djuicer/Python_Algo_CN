class BoothsAlgorithm:
    """
    Booth 算法寻找字符串在字典序下最小的循环移位。

    时间复杂度：O(n)，线性时间，n 为输入字符串长度
    空间复杂度：O(n)，失配函数数组需要线性空间

    更多信息：https://en.wikipedia.org/wiki/Booth%27s_multiplication_algorithm
    """

    def find_minimal_rotation(self, string: str) -> str:
        """
        寻找输入字符串在字典序下最小的循环移位。

        参数：
            string (str): 待求最小循环移位的输入字符串。

        返回：
            str: 输入字符串在字典序下最小的循环移位。

        异常：
            ValueError: 输入不是字符串或为空时抛出。

        示例：
            >>> ba = BoothsAlgorithm()
            >>> ba.find_minimal_rotation("baca")
            'abac'
            >>> ba.find_minimal_rotation("aaab")
            'aaab'
            >>> ba.find_minimal_rotation("abcd")
            'abcd'
            >>> ba.find_minimal_rotation("dcba")
            'adcb'
            >>> ba.find_minimal_rotation("aabaa")
            'aaaab'
        """
        if not isinstance(string, str) or not string:
            raise ValueError("Input must be a non-empty string")

        n = len(string)
        s = string + string  # 将字符串重复一遍，以处理所有循环移位
        f = [-1] * (2 * n)  # 初始化长度为原字符串两倍的失配函数数组
        k = 0  # 最小循环移位的起始位置

        for j in range(1, 2 * n):
            sj = s[j]
            i = f[j - k - 1]

            while i != -1 and sj != s[k + i + 1]:
                if sj < s[k + i + 1]:
                    k = j - i - 1
                i = f[i]

            if i == -1 and sj != s[k]:
                if sj < s[k]:
                    k = j
                f[j - k] = -1
            else:
                f[j - k] = i + 1

        return s[k : k + n]


if __name__ == "__main__":
    ba = BoothsAlgorithm()
    print(ba.find_minimal_rotation("bca"))  # 输出为 'abc'
