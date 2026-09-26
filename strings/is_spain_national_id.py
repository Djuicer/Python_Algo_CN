NUMBERS_PLUS_LETTER = "Input must be a string of 8 numbers plus letter"
LOOKUP_LETTERS = "TRWAGMYFPDXBNJZSQVHLCKE"


def is_spain_national_id(spanish_id: str) -> bool:
    """
    西班牙身份证号码由 8 个数字和一个字母组成
    该字母实际上用于校验，而非号码本身，
    可检查输入系统时是否出错，
    或是否提供了伪造号码。

    https://en.wikipedia.org/wiki/Documento_Nacional_de_Identidad_(Spain)#Number

    >>> is_spain_national_id("12345678Z")
    True
    >>> is_spain_national_id("12345678z")  # It is case-insensitive
    True
    >>> is_spain_national_id("12345678x")
    False
    >>> is_spain_national_id("12345678I")
    False
    >>> is_spain_national_id("12345678-Z")  # Some systems add a dash
    True
    >>> is_spain_national_id("12345678")
    Traceback (most recent call last):
        ...
    ValueError: Input must be a string of 8 numbers plus letter
    >>> is_spain_national_id("123456709")
    Traceback (most recent call last):
        ...
    ValueError: Input must be a string of 8 numbers plus letter
    >>> is_spain_national_id("1234567--Z")
    Traceback (most recent call last):
        ...
    ValueError: Input must be a string of 8 numbers plus letter
    >>> is_spain_national_id("1234Z")
    Traceback (most recent call last):
        ...
    ValueError: Input must be a string of 8 numbers plus letter
    >>> is_spain_national_id("1234ZzZZ")
    Traceback (most recent call last):
        ...
    ValueError: Input must be a string of 8 numbers plus letter
    >>> is_spain_national_id(12345678)
    Traceback (most recent call last):
        ...
    TypeError: Expected string as input, found int
    """

    if not isinstance(spanish_id, str):
        msg = f"Expected string as input, found {type(spanish_id).__name__}"
        raise TypeError(msg)

    spanish_id_clean = spanish_id.replace("-", "").upper()
    if len(spanish_id_clean) != 9:
        raise ValueError(NUMBERS_PLUS_LETTER)

    try:
        number = int(spanish_id_clean[0:8])
        letter = spanish_id_clean[8]
    except ValueError as ex:
        raise ValueError(NUMBERS_PLUS_LETTER) from ex

    if letter.isdigit():
        raise ValueError(NUMBERS_PLUS_LETTER)

    return letter == LOOKUP_LETTERS[number % 23]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
