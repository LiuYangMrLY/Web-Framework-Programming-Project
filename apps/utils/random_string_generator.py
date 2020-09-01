import datetime
import random
import string

from enum import Enum


class Pattern(Enum):
    Letters = string.ascii_letters
    Digits = string.digits
    Letters_And_Digits = string.ascii_letters + string.digits
    Uppercase = string.ascii_uppercase
    Lowercase = string.ascii_lowercase
    Hexdigits = string.hexdigits
    Uppercase_And_Digits = string.ascii_uppercase + string.digits
    Lowercase_And_Digits = string.ascii_lowercase + string.digits


def generate_string(length: int, pattern: Pattern = Pattern.Letters_And_Digits, use_time: bool = False) -> str:
    result = []

    if use_time:
        result.append(datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S_'))

    for i in range(length):
        result.append(random.choice(pattern.value))

    return ''.join(result)
