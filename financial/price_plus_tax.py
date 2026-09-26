"""
根据商品或服务的价格和税率计算含税价格。
"""


def price_plus_tax(price: float, tax_rate: float) -> float:
    """
    >>> price_plus_tax(100, 0.25)
    125.0
    >>> price_plus_tax(125.50, 0.05)
    131.775
    """
    return price * (1 + tax_rate)


if __name__ == "__main__":
    print(f"{price_plus_tax(100, 0.25) = }")
    print(f"{price_plus_tax(125.50, 0.05) = }")
