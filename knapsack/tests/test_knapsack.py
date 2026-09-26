"""
Created on Fri Oct 16 09:31:07 2020

@author: Dr. Tobias Schröder
@license: MIT-license

此文件包含背包问题的测试套件。
"""

import unittest

from knapsack import knapsack as k


class Test(unittest.TestCase):
    def test_base_case(self) -> None:
        """
        测试基本情况。
        """
        cap = 0
        val = [0]
        w = [0]
        c = len(val)
        assert k.knapsack(cap, w, val, c) == 0

        val = [60]
        w = [10]
        c = len(val)
        assert k.knapsack(cap, w, val, c) == 0

    def test_easy_case(self) -> None:
        """
        测试简单情况。
        """
        cap = 3
        val = [1, 2, 3]
        w = [3, 2, 1]
        c = len(val)
        assert k.knapsack(cap, w, val, c) == 5

    def test_knapsack(self) -> None:
        """
        测试背包问题。
        """
        cap = 50
        val = [60, 100, 120]
        w = [10, 20, 30]
        c = len(val)
        assert k.knapsack(cap, w, val, c) == 220

    def test_knapsack_repetition(self) -> None:
        """
        测试允许重复选取物品的背包问题。
        """
        cap = 50
        val = [60, 100, 120]
        w = [10, 20, 30]
        c = len(val)
        assert k.knapsack(cap, w, val, c, True) == 300


if __name__ == "__main__":
    unittest.main()
