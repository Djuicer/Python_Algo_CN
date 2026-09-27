"""
数位和数列
第 551 题

设 a(0), a(1),... 为如下定义的整数数列：
     a(0) = 1
     当 n >= 1 时，a(n) 是前一项各位数字之和

该数列从 1, 1, 2, 4, 8, ... 开始
已知 a(10^6) = 31054319。

求 a(10^15)
"""

ks = range(2, 20 + 1)
base = [10**k for k in range(ks[-1] + 1)]
memo: dict[int, dict[int, list[list[int]]]] = {}


def next_term(a_i, k, i, n):
    """
    就地计算并更新 a_i，使其成为第 n 项；或者当各项写成以下形式时，
    使其成为满足 c > 10^k 的最小项：
            a(i) = b * 10^k + c

    对于任意 a(i)，如果 digitsum(b) 与 c 的值相同，则在 c >= 10^k 之前，
    后续项之间的差值都相同。缓存此差值可大幅加快计算。

    参数：
    a_i -- 从个位开始、表示数列第 i 项的数字数组
    k --  将各项写成 a(i) = b*10^k + c 形式时的 k。
          计算各项，直到 c > 10^k 或到达第 n 项。
    i -- 数列中的位置
    n -- 当 k 足够大时要计算到的项

    返回：由结束项与起始项的差值以及计算的项数构成的元组。例如，若起始项
    为 a_0=1，结束项为 a_10=62，则返回 (61, 9)。
    """
    # ds_b - digitsum(b)
    ds_b = sum(a_i[j] for j in range(k, len(a_i)))
    c = sum(a_i[j] * base[j] for j in range(min(len(a_i), k)))

    diff, dn = 0, 0
    max_dn = n - i

    sub_memo = memo.get(ds_b)

    if sub_memo is not None:
        jumps = sub_memo.get(c)

        if jumps is not None and len(jumps) > 0:
            # 找到并执行不超过上限的最大跳跃
            max_jump = -1
            for _k in range(len(jumps) - 1, -1, -1):
                if jumps[_k][2] <= k and jumps[_k][1] <= max_dn:
                    max_jump = _k
                    break

            if max_jump >= 0:
                diff, dn, _kk = jumps[max_jump]
                # 由于缓存了跳跃之间的差值，因此加上 c
                new_c = diff + c
                for j in range(min(k, len(a_i))):
                    new_c, a_i[j] = divmod(new_c, 10)
                if new_c > 0:
                    add(a_i, k, new_c)

        else:
            sub_memo[c] = []
    else:
        sub_memo = {c: []}
        memo[ds_b] = sub_memo

    if dn >= max_dn or c + diff >= base[k]:
        return diff, dn

    if k > ks[0]:
        while True:
            # 继续执行较小的跳跃
            _diff, terms_jumped = next_term(a_i, k - 1, i + dn, n)
            diff += _diff
            dn += terms_jumped

            if dn >= max_dn or c + diff >= base[k]:
                break
    else:
        # 跳跃幅度会太小，改为依次计算各项
        _diff, terms_jumped = compute(a_i, k, i + dn, n)
        diff += _diff
        dn += terms_jumped

    jumps = sub_memo[c]

    # 按跳过的项数保持 jumps 有序
    j = 0
    while j < len(jumps):
        if jumps[j][1] > dn:
            break
        j += 1

    # 为 digitsum(b) 和 c 的当前值缓存该跳跃
    sub_memo[c].insert(j, (diff, dn, k))
    return (diff, dn)


def compute(a_i, k, i, n):
    """
    与 next_term(a_i, k, i, n) 相同，但计算各项时不记忆结果。
    """
    if i >= n:
        return 0, i
    if k > len(a_i):
        a_i.extend([0 for _ in range(k - len(a_i))])

    # 注意：a_i -> b * 10^k + c
    # ds_b -> digitsum(b)
    # ds_c -> digitsum(c)
    start_i = i
    ds_b, ds_c, diff = 0, 0, 0
    for j in range(len(a_i)):
        if j >= k:
            ds_b += a_i[j]
        else:
            ds_c += a_i[j]

    while i < n:
        i += 1
        addend = ds_c + ds_b
        diff += addend
        ds_c = 0
        for j in range(k):
            s = a_i[j] + addend
            addend, a_i[j] = divmod(s, 10)

            ds_c += a_i[j]

        if addend > 0:
            break

    if addend > 0:
        add(a_i, k, addend)
    return diff, i - start_i


def add(digits, k, addend) -> None:
    """
    从索引 k 开始，将 addend 加到 digits 给出的数字数组中。
    """
    for j in range(k, len(digits)):
        s = digits[j] + addend
        if s >= 10:
            quotient, digits[j] = divmod(s, 10)
            addend = addend // 10 + quotient
        else:
            digits[j] = s
            addend = addend // 10

        if addend == 0:
            break

    while addend > 0:
        addend, digit = divmod(addend, 10)
        digits.append(digit)


def solution(n: int = 10**15) -> int:
    """
    返回数列的第 n 项。

    >>> solution(10)
    62

    >>> solution(10**6)
    31054319

    >>> solution(10**15)
    73597483551591773
    """

    digits = [1]
    i = 1
    dn = 0
    while True:
        _diff, terms_jumped = next_term(digits, 20, i + dn, n)
        dn += terms_jumped
        if dn == n - i:
            break

    a_n = 0
    for j in range(len(digits)):
        a_n += digits[j] * 10**j
    return a_n


if __name__ == "__main__":
    print(f"{solution() = }")
