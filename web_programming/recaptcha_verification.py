"""
Recaptcha 是 Google 提供的免费验证码服务，用于保护网站和表单。可在
https://www.google.com/recaptcha/admin/create 创建新的 Recaptcha 密钥，并
查看已创建的密钥。
* 请注意，Recaptcha 不适用于 localhost
创建 Recaptcha 密钥时会得到两个独立密钥：ClientKey 和 SecretKey。
ClientKey 应保存在站点前端，SecretKey 应保存在站点后端。

# 下面展示带有 Recaptcha 标签的 HTML 登录表示例

    <form action="" method="post">
        <h2 class="text-center">Log in</h2>
        {% csrf_token %}
        <div class="form-group">
            <input type="text" name="username" required="required">
        </div>
        <div class="form-group">
            <input type="password" name="password" required="required">
        </div>
        <div class="form-group">
            <button type="submit">Log in</button>
        </div>
        <!-- Below is the recaptcha tag of html -->
        <div class="g-recaptcha" data-sitekey="ClientKey"></div>
    </form>

    <!-- Below is the recaptcha script to be kept inside html tag -->
    <script src="https://www.google.com/recaptcha/api.js" async defer></script>

下面的 Django 函数用于 views.py 文件，包含一个演示 Recaptcha 验证的登录表单。
"""

# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "httpx2",
# ]
# ///

import httpx2

try:
    from django.contrib.auth import authenticate, login
    from django.shortcuts import redirect, render
except ImportError:
    authenticate = login = render = redirect = print


def login_using_recaptcha(request):
    # 在此输入 Recaptcha 密钥
    secret_key = "secretKey"  # noqa: S105
    url = "https://www.google.com/recaptcha/api/siteverify"

    # 方法不是 POST 时，将用户转到登录页面
    if request.method != "POST":
        return render(request, "login.html")

    # 从前端获取 username、password 和 client_key
    username = request.POST.get("username")
    password = request.POST.get("password")
    client_key = request.POST.get("g-recaptcha-response")

    # 将 Recaptcha 响应发送到 Google Recaptcha API
    response = httpx2.post(
        url, data={"secret": secret_key, "response": client_key}, timeout=10
    )
    # Recaptcha API 验证密钥成功时
    if response.json().get("success", False):
        # 验证用户身份
        user_in_database = authenticate(request, username=username, password=password)
        if user_in_database:
            login(request, user_in_database)
            return redirect("/your-webpage")
    return render(request, "login.html")
