# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "httpx2",
# ]
# ///

import httpx2


# 获取 IP 地址地理位置数据的函数
def get_ip_geolocation(ip_address: str) -> str:
    try:
        # 构造 IP 地理位置 API 的 URL
        url = f"https://ipinfo.io/{ip_address}/json"

        # 向 API 发送 GET 请求
        response = httpx2.get(url, timeout=10)

        # 检查 HTTP 请求是否成功
        response.raise_for_status()

        # 将响应解析为 JSON
        data = response.json()

        # 检查城市、地区和国家信息是否可用
        if "city" in data and "region" in data and "country" in data:
            location = f"Location: {data['city']}, {data['region']}, {data['country']}"
        else:
            location = "Location data not found."

        return location
    except httpx2.RequestError as e:
        # 处理网络相关异常
        return f"Request error: {e}"
    except ValueError as e:
        # 处理 JSON 解析错误
        return f"JSON parsing error: {e}"


if __name__ == "__main__":
    # 提示用户输入 IP 地址
    ip_address = input("Enter an IP address: ")

    # 获取并输出地理位置数据
    location = get_ip_geolocation(ip_address)
    print(location)
