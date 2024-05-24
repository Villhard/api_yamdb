from string import ascii_letters, digits
from random import choices


def generate_code(length=16):
    """
    Генерация кода для подтверждения.
    """
    symbols = ascii_letters + digits
    return ''.join(choices(symbols, k=length))