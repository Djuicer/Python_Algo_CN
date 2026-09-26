import random


class Validator:
    def __init__(self, name: str, stake: int) -> None:
        """
        使用给定的名称和质押量初始化新的验证者。

        参数：
            name (str): 验证者的名称。
            stake (int): 验证者拥有的质押量。
        """
        self.name = name
        self.stake = stake


def choose_validator(validators: list[Validator]) -> Validator:
    """
    根据质押量的权重选择一名验证者来创建下一个区块。

    质押量越高，被选中的概率越大。

    参数：
        validators (list[Validator]): Validator 对象列表。

    返回：
        Validator: 通过加权随机选择得到的验证者。

    示例：
        >>> validators = [Validator("Alice", 50), Validator("Bob", 30)]
        >>> chosen = choose_validator(validators)
        >>> isinstance(chosen, Validator)
        True
    """
    total_stake = sum(v.stake for v in validators)
    weighted_validators = [(v, v.stake / total_stake) for v in validators]
    selected = random.choices(
        [v[0] for v in weighted_validators], weights=[v[1] for v in weighted_validators]
    )
    return selected[0]
