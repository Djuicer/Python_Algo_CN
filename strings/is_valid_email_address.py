"""
实现电子邮箱地址有效性验证算法

@ https://en.wikipedia.org/wiki/Email_address
"""

import string

email_tests: tuple[tuple[str, bool], ...] = (
    ("simple@example.com", True),
    ("very.common@example.com", True),
    ("disposable.style.email.with+symbol@example.com", True),
    ("other-email-with-hyphen@and.subdomains.example.com", True),
    ("fully-qualified-domain@example.com", True),
    ("user.name+tag+sorting@example.com", True),
    ("x@example.com", True),
    ("example-indeed@strange-example.com", True),
    ("test/test@test.com", True),
    (
        "123456789012345678901234567890123456789012345678901234567890123@example.com",
        True,
    ),
    ("admin@mailserver1", True),
    ("example@s.example", True),
    ("Abc.example.com", False),
    ("A@b@c@example.com", False),
    ("abc@example..com", False),
    ("a(c)d,e:f;g<h>i[j\\k]l@example.com", False),
    (
        "12345678901234567890123456789012345678901234567890123456789012345@example.com",
        False,
    ),
    ("i.like.underscores@but_its_not_allowed_in_this_part", False),
    ("", False),
)

# The maximum octets (one character as a standard unicode character is one byte)
# that the local part and the domain part can have
MAX_LOCAL_PART_OCTETS = 64
MAX_DOMAIN_OCTETS = 255


def is_valid_email_address(email: str) -> bool:
    """
    传入的邮箱地址有效时返回 True。

    邮箱的本地部分位于唯一的 @ 符号之前，
    与显示名称关联，例如 "john.smith"。
    域名部分位于 @ 之后，其规则比本地部分更严格。

    邮箱整体检查：
     1. 邮箱地址只能有一个 @ 符号。严格来说，若本地部分的
        @ 符号被引号包围，则也是有效的，但此
        实现暂不处理 ""。
        (See https://en.wikipedia.org/wiki/Email_address#:~:text=If%20quoted,)
     2. The local-part and the domain are limited to a certain number of octets. With
        unicode storing a single character in one byte, each octet is equivalent to
        a character. Hence, we can just check the length of the string.
    本地部分检查：
     3. 本地部分可以包含大小写拉丁字母、数字 0 到 9，
        以及可打印字符 (!#$%&'*+-/=?^_`{|}~)
     4. 本地部分的 "." 可以出现在首尾以外的位置，
        但不能连续出现多个 "."。

    域名部分检查：
     5. 域名可以包含大小写拉丁字母和数字 0 到 9
     6. 可以包含连字符 "-"，但不能位于首尾
     7. 域名中的 "." 可以出现在首尾以外的位置，
        但不能连续出现多个 "."。

    >>> for email, valid in email_tests:
    ...     assert is_valid_email_address(email) == valid
    """

    # （1.）确保邮箱地址中仅有一个 @ 符号
    if email.count("@") != 1:
        return False

    local_part, domain = email.split("@")
    # （2.）检查本地部分和域名的字节长度
    if len(local_part) > MAX_LOCAL_PART_OCTETS or len(domain) > MAX_DOMAIN_OCTETS:
        return False

    # （3.）验证本地部分的字符
    if any(
        char not in string.ascii_letters + string.digits + ".(!#$%&'*+-/=?^_`{|}~)"
        for char in local_part
    ):
        return False

    # （4.）验证本地部分中 "." 的位置
    if local_part.startswith(".") or local_part.endswith(".") or ".." in local_part:
        return False

    # （5.）验证域名中的字符
    if any(char not in string.ascii_letters + string.digits + ".-" for char in domain):
        return False

    # （6.）验证 "-" 的位置
    if domain.startswith("-") or domain.endswith("."):
        return False

    # （7.）验证 "." 的位置
    return not (domain.startswith(".") or domain.endswith(".") or ".." in domain)


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    for email, valid in email_tests:
        is_valid = is_valid_email_address(email)
        assert is_valid == valid, f"{email} is {is_valid}"
        print(f"Email address {email} is {'not ' if not is_valid else ''}valid")
