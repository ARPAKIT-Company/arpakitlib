from random import randint


def generate_simple_code(
        *,
        amount: int = 5
) -> str:
    letters = "JZSDQWRLGFZ123456789"
    alphabet: list = list(letters.lower() + letters.upper())
    return "".join(alphabet[randint(0, len(alphabet) - 1)] for _ in range(amount))


def __example():
    pass


if __name__ == '__main__':
    __example()
