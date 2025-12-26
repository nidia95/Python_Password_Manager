import getpass
from dt_security import (
    encrypt_text,
    decrypt_text,
    validate_password_strength,
)

# Example usage
if __name__ == "__main__":
    print("=" * 60)
    print("QUANTUM-RESISTANT ENCRYPTION (AES-256-GCM)")
    print("=" * 60)
    print("\nSecurity Note:")
    print("- AES-256 provides ~128-bit quantum resistance")
    print("- Grover's algorithm reduces effective strength by half")
    print("- Still secure against current and near-future quantum computers")
    print("=" * 60 + "\n")

    # Sample text to encrypt
    original_text: str = """This is a highly confidential message that needs 
protection against quantum computer attacks. AES-256 provides 
sufficient security for the next 20-30 years."""

    print("Original Text:")
    print(f'"{original_text}"')
    print("\n" + "=" * 60 + "\n")

    # Get password for encryption
    while True:
        password: str = getpass.getpass(
            prompt="Enter password for encryption (min 16 chars): "
        )
        is_valid, message = validate_password_strength(password=password)
        if is_valid:
            print(f"✓ {message}\n")
            break
        else:
            print(f"✗ {message}\n")

    # Encrypt the text
    print("Encrypting...")
    encrypted_data: dict = encrypt_text(plaintext=original_text, password=password)

    print("\nEncrypted Data:")
    print(f"Salt: {encrypted_data['salt'][:32]}...")
    print(f"Nonce: {encrypted_data['nonce'][:32]}...")
    print(f"Ciphertext: {encrypted_data['ciphertext'][:50]}...")
    print(f"Auth Tag: {encrypted_data['tag']}")
    print("\n" + "=" * 60 + "\n")

    # Get password for decryption
    password_decrypt: str = getpass.getpass(prompt="Enter password for decryption: ")

    # Decrypt the text
    print("\nDecrypting...")

    is_decrypted: bool
    plaintext: str
    is_decrypted, plaintext = decrypt_text(
        encrypted_data=encrypted_data, password=password_decrypt
    )
    if is_decrypted:
        print("\n✓ Decryption Successful!")
        print("\nDecrypted Text:")
        print(f'"{plaintext}"')

        # Verify integrity
        if plaintext == original_text:
            print("\n✓ Data integrity verified - No tampering detected")
    else:
        print("\n✗ Decryption Failed!")
        print(f"\nError:")
        print(f'"{plaintext}"')
