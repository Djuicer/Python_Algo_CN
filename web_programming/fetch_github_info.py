#!/usr/bin/env python3
"""
Created by sarathkaul on 14/11/19
Updated by lawric1 on 24/11/20

通过访问令牌进行身份验证。
访问 https://github.com/settings/tokens 生成个人访问令牌。

注意：
切勿在代码中硬编码凭据。应始终使用环境文件保存私密信息，并在运行时使用
`os` 模块获取这些信息。

在根目录创建 ".env" 文件，并将令牌写入以下两行：

#!/usr/bin/env bash
export USER_TOKEN=""
"""

# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "httpx2",
# ]
# ///

from __future__ import annotations

import os
from typing import Any

import httpx2

BASE_URL = "https://api.github.com"

# https://docs.github.com/en/free-pro-team@latest/rest/reference/users#get-the-authenticated-user
AUTHENTICATED_USER_ENDPOINT = BASE_URL + "/user"

# https://github.com/settings/tokens
USER_TOKEN = os.environ.get("USER_TOKEN", "")


def fetch_github_info(auth_token: str) -> dict[Any, Any]:
    """
    使用 httpx2 模块获取 GitHub 用户信息。
    """
    headers = {
        "Authorization": f"token {auth_token}",
        "Accept": "application/vnd.github.v3+json",
    }
    return httpx2.get(AUTHENTICATED_USER_ENDPOINT, headers=headers, timeout=10).json()


if __name__ == "__main__":  # pragma: no cover
    if USER_TOKEN:
        for key, value in fetch_github_info(USER_TOKEN).items():
            print(f"{key}: {value}")
    else:
        raise ValueError("'USER_TOKEN' field cannot be empty.")
