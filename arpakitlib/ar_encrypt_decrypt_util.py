# arpakit

from cryptography.fernet import Fernet

_ARPAKIT_LIB_MODULE_VERSION = "3.0"


def generate_secret_key() -> str:
    return Fernet.generate_key().decode()


def encrypt_with_secret_key(string: str, secret_key: str) -> str:
    return Fernet(secret_key.encode()).encrypt(string.encode()).decode()


def decrypt_with_secret_key(string: str, secret_key: str) -> str:
    return Fernet(secret_key.encode()).decrypt(string.encode()).decode()


def __example():
    secret_key = generate_secret_key()
    print(secret_key)

    original_string = "Hello World"
    encrypted_string = encrypt_with_secret_key(string=original_string, secret_key=secret_key)
    print(encrypted_string)

    decrypted_string = decrypt_with_secret_key(string=encrypted_string, secret_key=secret_key)
    print(decrypted_string)

    print(True) if original_string == decrypted_string else print(False)

if __name__ == '__main__':
    __example()
