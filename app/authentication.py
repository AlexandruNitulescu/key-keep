from sqlalchemy.orm import Session
from models import User, KeyKeeper
import bcrypt
from cryptography.fernet import Fernet
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
import os

def verify_password(plain_password: str, hashed_password: str) -> bool:
    password_byte_enc = plain_password.encode('utf-8')
    return bcrypt.checkpw(password = password_byte_enc , hashed_password = hashed_password)

def get_password_hash(password: str) -> str:
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    return hashed_password

def authenticate_user(username: str, password: str, db: Session):
    user = db.query(User).filter(User.username == username).first()
    
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def register_user(username: str, password: str, password_repeat: str, db: Session):
    user = db.query(User).filter(User.username == username).first()
    if user:
        return "Username already exists."
    if len(username) <= 3:
        return "Username should be longer than 3 characters!"
    if len(password) < 6:
        return "Password should be longer than 6 characters!"
    if password != password_repeat:
        return "Passwords do not match."

    hashed_password = get_password_hash(password)

    new_user = User(username=username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.close()
    
    return True

def get_own_keys(user_id, db: Session):
    key_keepers = db.query(KeyKeeper).filter(KeyKeeper.user_id == user_id).all()
    return key_keepers



# def generate_key(user_password):
#     if isinstance(user_password, str):  # Check if user_password is a string
#         user_password_bytes = user_password.encode()  # Encode string to bytes
#     else:
#         user_password_bytes = user_password  # Use user_password directly if it's already bytes
#     # Generate a Fernet key using the user's password
#     key = base64.urlsafe_b64encode(user_password_bytes)
#     # Ensure the key is 32 bytes long (if not, pad it with '=' characters)
#     while len(key) % 4 != 0:
#         key += b'='
#     return key

def generate_fernet_key(password):
    if isinstance(password, str):  # Check if password is a string
        password_bytes = password.encode()  # Encode string to bytes
    else:
        password_bytes = password  # Use password directly if it's already bytes

    salt = os.urandom(16)

    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),
                     length=32,  # Fernet keys are 32 bytes
                     salt=salt,
                     iterations=100000,
                     backend=default_backend())
    key = base64.urlsafe_b64encode(kdf.derive(password_bytes))
    fern = Fernet(key)

    # Optionally, return the key and salt for storage
    return key, salt

def encrypt_data(data, key):
    # Generate Fernet cipher suite using the key
    cipher_suite = Fernet(key)
    # Encrypt the data
    encrypted_data = cipher_suite.encrypt(data.encode())
    return encrypted_data

def decrypt_data(encrypted_data, key):
    # Generate Fernet cipher suite using the key
    cipher_suite = Fernet(key)
    # Decrypt the data
    decrypted_data = cipher_suite.decrypt(encrypted_data).decode()
    return decrypted_data







