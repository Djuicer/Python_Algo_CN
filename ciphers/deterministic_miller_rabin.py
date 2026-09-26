"""Created by Nathan Damon, @bizzfitch on github
>>> test_miller_rabin()
"""


def miller_rabin(n: int, allow_probable: bool = False) -> bool:
    """适用于约小于 3.32e24 的素数的确定性 Miller-Rabin 算法。

    使用数值分析结果判断传入数字是否为素数。如果数字超过上限且 allow_probable
    为 True，则返回 True 表示 n 可能是素数。此测试不会产生假阴性：返回 False
    始终表示合数。

    参数
    ----------
    n : int
        待测试的整数。由于通常关注数字是否为素数，n < 2 时返回 False，而不引发
        ValueError。
    allow_probable: bool, default False
        是否测试超过确定性测试上限的 n。

    异常
    ------
    ValueError

    参考资料
    ---------
    https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test
    """
    if n == 2:
        return True
    if not n % 2 or n < 2:
        return False
    if n > 5 and n % 10 not in (1, 3, 7, 9):  # 可快速检查末位数字
        return False
    if n > 3_317_044_064_679_887_385_961_981 and not allow_probable:
        raise ValueError(
            "Warning: upper bound of deterministic test is exceeded. "
            "Pass allow_probable=True to allow probabilistic test. "
            "A return value of True indicates a probable prime."
        )
    # 分析得出的数组边界
    bounds = [
        2_047,
        1_373_653,
        25_326_001,
        3_215_031_751,
        2_152_302_898_747,
        3_474_749_660_383,
        341_550_071_728_321,
        1,
        3_825_123_056_546_413_051,
        1,
        1,
        318_665_857_834_031_151_167_461,
        3_317_044_064_679_887_385_961_981,
    ]

    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]
    for idx, _p in enumerate(bounds, 1):
        if n < _p:
            # 此时得到最后一个需要检查的素数
            plist = primes[:idx]
            break
    d, s = n - 1, 0
    # 将 n - 1 分解为 2 的幂（s）和剩余奇数部分，即求解 d * 2 ** s == n - 1
    while d % 2 == 0:
        d //= 2
        s += 1
    for prime in plist:
        pr = False
        for r in range(s):
            m = pow(prime, d * 2**r, n)
            # m 的分析说明参见文章
            if (r == 0 and m == 1) or ((m + 1) % n == 0):
                pr = True
                # 此循环不会判定合数性
                break
        if pr:
            continue
        # 如果 pr 为 False，则上述循环从未得到真值，n 必为合数
        return False
    return True


def test_miller_rabin() -> None:
    """在每个范围内测试一个非平凡（末位为 1、3、7、9）合数和一个素数。
    """
    assert not miller_rabin(561)
    assert miller_rabin(563)
    # 2047

    assert not miller_rabin(838_201)
    assert miller_rabin(838_207)
    # 1_373_653

    assert not miller_rabin(17_316_001)
    assert miller_rabin(17_316_017)
    # 25_326_001

    assert not miller_rabin(3_078_386_641)
    assert miller_rabin(3_078_386_653)
    # 3_215_031_751

    assert not miller_rabin(1_713_045_574_801)
    assert miller_rabin(1_713_045_574_819)
    # 2_152_302_898_747

    assert not miller_rabin(2_779_799_728_307)
    assert miller_rabin(2_779_799_728_327)
    # 3_474_749_660_383

    assert not miller_rabin(113_850_023_909_441)
    assert miller_rabin(113_850_023_909_527)
    # 341_550_071_728_321

    assert not miller_rabin(1_275_041_018_848_804_351)
    assert miller_rabin(1_275_041_018_848_804_391)
    # 3_825_123_056_546_413_051

    assert not miller_rabin(79_666_464_458_507_787_791_867)
    assert miller_rabin(79_666_464_458_507_787_791_951)
    # 318_665_857_834_031_151_167_461

    assert not miller_rabin(552_840_677_446_647_897_660_333)
    assert miller_rabin(552_840_677_446_647_897_660_359)
    # 3_317_044_064_679_887_385_961_981
    # upper limit for probabilistic test


if __name__ == "__main__":
    test_miller_rabin()
