import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7
from cryptography.hazmat.backends import default_backend

KEY = b'0123456789abcdef0123456789abcdef'

def encrypt_message(message: str):
    iv = os.urandom(16)

    padder = PKCS7(128).padder()
    padded_data = padder.update(message.encode()) + padder.finalize()

    cipher = Cipher(algorithms.AES(KEY), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    return iv + ciphertext


def decrypt_message(data: bytes):
    iv = data[:16]
    ciphertext = data[16:]

    cipher = Cipher(algorithms.AES(KEY), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    padded_data = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = PKCS7(128).unpadder()
    message = unpadder.update(padded_data) + unpadder.finalize()

    return message.decode()