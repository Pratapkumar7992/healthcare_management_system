from cryptography.fernet import Fernet

# Generate a new key
YOUR_ENCRYPTION_KEY = Fernet.generate_key()

# Print the key so you can set it as an environment variable
print(YOUR_ENCRYPTION_KEY.decode())
