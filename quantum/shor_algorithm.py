import math
import random

"""
Shor 算法是基础量子计算算法之一，可通过找出用于生成公钥值 n 的素数来破解
RSA 密码协议。

本实现采用非常简单的结构，不使用 qiskit 或 cirq，以帮助理解 Shor 算法思想
的实际工作方式。

Shor 算法参考网站：
https://www.geeksforgeeks.org/shors-factorization-algorithm/

"""


class Shor:
    def period_find(self, num: int, number: int) -> int:
        """
        求 a^x mod N 的周期。

        >>> shor = Shor()
        >>> shor.period_find(2, 15)
        4
        >>> shor.period_find(3, 7)
        6
        """
        start: int = 1
        while pow(num, start, number) != 1:
            start += 1
        return start

    def shor_algorithm(self, number: int) -> tuple[int, int]:
        """
        运行 Shor 算法分解一个数。
        >>> shor = Shor()
        >>> random.seed(0)
        >>> factors = shor.shor_algorithm(15)
        >>> isinstance(factors, tuple) and len(factors) == 2
        True
        >>> factors
        (3, 5)
        """
        if number % 2 == 0:
            return 2, number // 2
        while True:
            random.seed(0)
            num: int = random.randint(2, number - 1)
            gcd_number_num: int = math.gcd(number, num)
            if gcd_number_num > 1:
                return gcd_number_num, number // gcd_number_num

            result: int = self.period_find(num, number)
            if not result % 2:
                start: int = pow(num, result // 2, number)
                if start != number - 1:
                    p_value: int = math.gcd(start - 1, number)
                    q_value: int = math.gcd(start + 1, number)
                    if p_value > 1 and q_value > 1:
                        return p_value, q_value


if __name__ == "__main__":
    shor = Shor()
    print(shor.shor_algorithm(15))
