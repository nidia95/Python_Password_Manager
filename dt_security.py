"""
DT Security
"""

import os
import random
import string
import base64

from typing import Tuple

from cryptography.hazmat.backends import default_backend

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import modes
from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers import algorithms

# from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


__version__ = "1.0.0"


def generate_password(length: int = 24) -> str:
    """
    Generate a secure password with a specified length

    Args:
        length (int): Password length (minimum 4 characters)

    Returns:
        str: Generated password
    """

    if length < 4:
        message: str = "Password length must be at least 4 characters!"
        raise ValueError(message)

    # Define character sets
    digit: str = string.digits  # numbers
    special: str = string.punctuation  # special characters
    lowercase: str = string.ascii_lowercase  # lowercase letters
    uppercase: str = string.ascii_uppercase  # uppercase letters

    # Ensure at least one character from each type
    password = [
        random.choice(seq=digit),
        random.choice(seq=special),
        random.choice(seq=lowercase),
        random.choice(seq=uppercase),
    ]

    # Fill the rest of the password with random characters
    all_characters = digit + special + lowercase + uppercase
    password += random.choices(
        k=length - 4,
        population=all_characters,
    )

    # Shuffle the characters
    random.shuffle(x=password)

    result: str = "".join(password)
    return result


def derive_key_from_password(password: str, salt: bytes) -> bytes:
    """
    Derive a 256-bit encryption key from password using PBKDF2

    Args:
        password (str): User's password
        salt (bytes): 16-byte random salt for key derivation

    Returns:
        bytes: 32-byte (256-bit) key for AES-256
    """

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,  # 256 bits for AES-256
        salt=salt,
        iterations=600_000,  # OWASP recommendation (2023+)
        backend=default_backend(),
    )

    return kdf.derive(password.encode("utf-8"))


def encrypt_text(plaintext: str, password: str) -> dict:
    """
    Encrypt text using AES-256-GCM (Quantum-resistant symmetric encryption)

    AES-256 provides approximately 128-bit security against quantum computers
    (Grover's algorithm reduces effective key length by half)

    Args:
        plaintext (str): Text to encrypt
        password (str): User's password (minimum 16 characters recommended)

    Returns:
        dict: Contains salt, nonce, ciphertext, and authentication tag
    """

    # Generate random salt (16 bytes)
    salt = os.urandom(16)

    # Derive 256-bit key from password
    key = derive_key_from_password(password=password, salt=salt)

    # Generate random nonce (12 bytes for GCM)
    nonce = os.urandom(12)

    # Create AES-256-GCM cipher
    cipher = Cipher(
        algorithm=algorithms.AES(key=key),
        mode=modes.GCM(initialization_vector=nonce),
        backend=default_backend(),
    )
    encryptor = cipher.encryptor()

    # Encrypt the plaintext
    ciphertext = encryptor.update(data=plaintext.encode("utf-8")) + encryptor.finalize()

    # Get authentication tag (prevents tampering)
    tag = encryptor.tag

    # Return all components needed for decryption
    return {
        "salt": base64.b64encode(salt).decode("utf-8"),
        "nonce": base64.b64encode(nonce).decode("utf-8"),
        "ciphertext": base64.b64encode(ciphertext).decode("utf-8"),
        "tag": base64.b64encode(tag).decode("utf-8"),
    }


def decrypt_text(encrypted_data: dict, password: str) -> Tuple[bool, str]:
    """
    Decrypt text encrypted with AES-256-GCM

    Args:
        encrypted_data (dict): Dictionary containing salt, nonce, ciphertext, tag
        password (str): User's password (must match encryption password)

    Returns:
        Tuple[bool, str]: True if decryption was successful, False otherwise

    Raises:
        Exception: If password is wrong, data is corrupted, or tampered
    """

    try:
        # Decode Base64 components
        salt = base64.b64decode(encrypted_data["salt"])
        nonce = base64.b64decode(encrypted_data["nonce"])
        ciphertext = base64.b64decode(encrypted_data["ciphertext"])
        tag = base64.b64decode(encrypted_data["tag"])

        # Derive the same key from password and salt
        key = derive_key_from_password(password=password, salt=salt)

        # Create AES-256-GCM cipher with authentication tag
        cipher = Cipher(
            algorithm=algorithms.AES(key=key),
            mode=modes.GCM(initialization_vector=nonce, tag=tag),
            backend=default_backend(),
        )
        decryptor = cipher.decryptor()

        # Decrypt and verify authentication
        plaintext = decryptor.update(data=ciphertext) + decryptor.finalize()

        return True, plaintext.decode("utf-8")

    except Exception as e:
        return (
            False,
            f"Decryption failed! Wrong password or data corrupted/tampered",
        )


def validate_password_strength(password: str) -> Tuple[bool, str]:
    """
    Check if password is strong enough for quantum-resistant encryption

    Args:
        password (str): Password to validate

    Returns:
        tuple: (is_valid: bool, message: str)
    """
    if len(password) < 16:
        return False, "Password must be at least 16 characters for quantum resistance"

    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(not c.isalnum() for c in password)

    if not (has_upper and has_lower and has_digit and has_special):
        return (
            False,
            "Password must contain uppercase, lowercase, digits, and special characters",
        )

    return True, "Password is strong"


if __name__ == "__main__":
    print("[-] This module is not meant to be run directly!")
