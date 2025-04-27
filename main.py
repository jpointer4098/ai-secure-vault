from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os

load_dotenv()

encryption_key = os.getenv("ENCRYPTION_KEY")
vault_file = "vault.enc"

def generate_key():
    return Fernet.generate_key().decode()

def encrypt_data(key, data):
    fernet = Fernet(key.encode())
    return fernet.encrypt(data.encode())

def decrypt_data(key, data):
    fernet = Fernet(key.encode())
    return fernet.decrypt(data).decode()

def save_encrypted_data(encrypted_data):
    with open(vault_file, "wb") as file:
        file.write(encrypted_data)

def load_encrypted_data():
    if not os.path.exists(vault_file):
        return None
    with open(vault_file, "rb") as file:
        return file.read()

def main():
    if not encryption_key:
        print("Encryption key not found. Generate one and set it in .env.")
        return

    choice = input("Enter '1' to store a new API key, '2' to retrieve it: ").strip()

    if choice == "1":
        api_key = input("Enter the API key to store securely: ").strip()
        encrypted = encrypt_data(encryption_key, api_key)
        save_encrypted_data(encrypted)
        print("API key encrypted and stored successfully.")
    elif choice == "2":
        encrypted_data = load_encrypted_data()
        if encrypted_data:
            decrypted = decrypt_data(encryption_key, encrypted_data)
            print(f"Retrieved API key: {decrypted}")
        else:
            print("No encrypted data found.")
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
