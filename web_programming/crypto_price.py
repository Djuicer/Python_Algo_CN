"""
使用 CoinGecko 的实时价格数据将 ETH 换算为 USD。
"""

# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "httpx2",
# ]
# ///

from httpx2 import get

COINGECKO_URL = (
    "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"
)


def get_eth_price_usd() -> float:
    """获取当前以 USD 计价的 ETH 价格。"""
    return get(COINGECKO_URL, timeout=10).raise_for_status().json()["ethereum"]["usd"]


def eth_to_usd(eth_amount: float) -> float:
    """将 ETH 数量换算为 USD。"""
    return eth_amount * get_eth_price_usd()


if __name__ == "__main__":
    eth_amount = float(input("Enter ETH amount: "))
    usd_value = eth_to_usd(eth_amount)
    print(f"{eth_amount} ETH = ${usd_value:.2f} USD")
