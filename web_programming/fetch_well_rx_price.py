"""

提供药品名称和邮政编码后，从 rx 站点抓取处方药价格和药房名称。

"""

import httpx2
from bs4 import BeautifulSoup

BASE_URL = "https://www.wellrx.com/prescriptions/{}/{}/?freshSearch=true"


def fetch_pharmacy_and_price_list(drug_name: str, zip_code: str) -> list | None:
    """[摘要]

    本函数接收药品名称和邮政编码，随后请求 BASE_URL 站点。获取页面数据并
    抓取，生成该处方药最低价格列表。

    参数：
        drug_name (str): [药品名称]
        zip_code(str): [邮政编码]

    返回：
        list: [药房名称和价格的列表]

    >>> print(fetch_pharmacy_and_price_list(None, None))
    None
    >>> print(fetch_pharmacy_and_price_list(None, 30303))
    None
    >>> print(fetch_pharmacy_and_price_list("eliquis", None))
    None
    """

    try:
        # 用户是否提供了两个输入？
        if not drug_name or not zip_code:
            return None

        request_url = BASE_URL.format(drug_name, zip_code)
        response = httpx2.get(request_url, timeout=10).raise_for_status()

        # 使用 bs4 抓取数据
        soup = BeautifulSoup(response.text, "html.parser")

        # 此列表存储名称和价格
        pharmacy_price_list = []

        # 获取包含条目的所有网格
        grid_list = soup.find_all("div", {"class": "grid-x pharmCard"})
        if grid_list and len(grid_list) > 0:
            for grid in grid_list:
                # 获取药房价格
                pharmacy_name = grid.find("p", {"class": "list-title"}).text

                # 获取药品价格
                price = grid.find("span", {"p", "price price-large"}).text

                pharmacy_price_list.append(
                    {
                        "pharmacy_name": pharmacy_name,
                        "price": price,
                    }
                )

        return pharmacy_price_list

    except httpx2.HTTPError, ValueError:
        return None


if __name__ == "__main__":
    # 输入药品名称和邮政编码
    drug_name = input("Enter drug name: ").strip()
    zip_code = input("Enter zip code: ").strip()

    pharmacy_price_list: list | None = fetch_pharmacy_and_price_list(
        drug_name, zip_code
    )

    if pharmacy_price_list:
        print(f"\nSearch results for {drug_name} at location {zip_code}:")
        for pharmacy_price in pharmacy_price_list:
            name = pharmacy_price["pharmacy_name"]
            price = pharmacy_price["price"]

            print(f"Pharmacy: {name} Price: {price}")
    else:
        print(f"No results found for {drug_name}")
