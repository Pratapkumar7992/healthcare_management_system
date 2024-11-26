import bcrypt
from Crypto.Cipher import AES
import base64
import os
from cryptography.fernet import Fernet
YOUR_ENCRYPTION_KEY = os.urandom(16)

def encrypt_password(password):
    """Encrypt the password using bcrypt."""
    password_bytes = password.encode('utf-8')  # Convert to bytes
    salt = bcrypt.gensalt()  # Generate a salt means(any string like $f^%#fhdfvW#$gesdfs3#$%)
    hashed_password = bcrypt.hashpw(password_bytes, salt)  # Hash the password with the salt(bytes password and $f^%#fhdfvW#$gesdfs3#$%)
    return hashed_password.decode('utf-8')  # Return the hashed password as a string(return to the app.py)

def decrypt_password(hashed_password, password):
    """Check if the provided password matches the encrypted password."""
    password_bytes = password.encode('utf-8')  # Convert to bytes (original password is convert into bytes)
    hashed_password_bytes = hashed_password.encode('utf-8')  # Convert hashed password to bytes
    return bcrypt.checkpw(password_bytes, hashed_password_bytes)   # (checking wheather the bytes_password is same as hashed bytes_password)



# Load the key from the file
with open('secret.key', 'rb') as key_file:
    key = key_file.read()

fernet = Fernet(key)

def encrypt_data(data, key):
    cipher = Fernet(key)
    encrypted_data = cipher.encrypt(data.encode('utf-8'))
    return encrypted_data.decode('utf-8')

def decrypt_data(encrypted_data, key):
    cipher = Fernet(key)
    decrypted_data = cipher.decrypt(encrypted_data.encode('utf-8'))
    return decrypted_data.decode('utf-8')








