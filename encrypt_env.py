from cryptography.fernet import Fernet
import os

# Generate a secret key and save it (Run this once and store the key safely)
def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

# Encrypt the .env file
def encrypt_env():
    # Load the key
    with open("secret.key", "rb") as key_file:
        key = key_file.read()
    
    fernet = Fernet(key)
    
    # Read the .env file
    with open(".env", "rb") as env_file:
        env_data = env_file.read()
    
    # Encrypt and save it
    encrypted_data = fernet.encrypt(env_data)
    with open(".env.enc", "wb") as encrypted_file:
        encrypted_file.write(encrypted_data)
    
    print("✅ .env file encrypted successfully! Delete the original .env file for security.")

if __name__ == "__main__":
    generate_key()  # Run this once to create the key
    encrypt_env()
