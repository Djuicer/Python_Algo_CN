from __future__ import annotations


def stable_matching(
    donor_pref: list[list[int]], recipient_pref: list[list[int]]
) -> list[int]:
    """
    找到任何二分图中的稳定匹配，即没有 2 个对象的配对
    比起伴侣更喜欢对方。  该功能接受的偏好
    oegan 转让者和接受者（两者都分配有从 0 到 n-1 的编号）以及
    返回一个列表，其中索引位置对应于捐赠者和值
    索引是器官接受者。

    为了更好地理解该算法，另请参阅：
    https://github.com/akashvshroff/Gale_Shapley_Stable_Matching (README).
    https://www.youtube.com/watch?v=Qcv1IqHWAzg&t=13s (Numberphile YouTube).

    >>> donor_pref = [[0, 1, 3, 2], [0, 2, 3, 1], [1, 0, 2, 3], [0, 3, 1, 2]]
    >>> recipient_pref = [[3, 1, 2, 0], [3, 1, 0, 2], [0, 3, 1, 2], [1, 0, 3, 2]]
    >>> stable_matching(donor_pref, recipient_pref)
    [1, 2, 3, 0]
    """
    assert len(donor_pref) == len(recipient_pref)

    n = len(donor_pref)
    unmatched_donors = list(range(n))
    donor_record = [-1] * n  # 捐赠者捐赠给了谁
    rec_record = [-1] * n  # 收件人从谁那里收到的
    num_donations = [0] * n

    while unmatched_donors:
        donor = unmatched_donors[0]
        donor_preference = donor_pref[donor]
        recipient = donor_preference[num_donations[donor]]
        num_donations[donor] += 1
        rec_preference = recipient_pref[recipient]
        prev_donor = rec_record[recipient]

        if prev_donor != -1:
            if rec_preference.index(prev_donor) > rec_preference.index(donor):
                rec_record[recipient] = donor
                donor_record[donor] = recipient
                unmatched_donors.append(prev_donor)
                unmatched_donors.remove(donor)
        else:
            rec_record[recipient] = donor
            donor_record[donor] = recipient
            unmatched_donors.remove(donor)
    return donor_record
