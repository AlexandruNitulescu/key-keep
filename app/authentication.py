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


def authenticate_secret_key(username_id, secret_key, db: Session):
    user = db.query(User).filter(User.id == username_id).first()
    if user:
        if verify_secret_key(secret_key, user.hashed_secret_key):
            print("Secret key verified")
            print(type(secret_key))
            return True
        else:
            print("Secret key verification failed")
            print(type(secret_key))
            return False
    else:
        print("User not found")
        print(type(secret_key))

        return False


def verify_secret_key(secret_key: str, hashed_secret_key: str) -> bool:
    password_byte_enc = secret_key.encode('utf-8')
    return bcrypt.checkpw(password = password_byte_enc , hashed_password = hashed_secret_key)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    password_byte_enc = plain_password.encode('utf-8')
    return bcrypt.checkpw(password = password_byte_enc , hashed_password = hashed_password)

def get_password_hash(password: str) -> str:
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    
    return hashed_password

def get_secret_key_hash(secret_key: bytes) -> bytes:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=secret_key, salt=salt)
    
    return hashed_password


def authenticate_user(username: str, password: str, db: Session):
    user = db.query(User).filter(User.username == username).first()
    
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def register_user(username: str, password: str, password_repeat: str, db: Session):
    # Check username length and existence
    if len(username) <= 3:
        return False, "Username should be longer than 3 characters!"
    
    # Check password length and match
    if len(password) < 6:
        return False, "Password should be longer than 6 characters!"
    elif password != password_repeat:
        return False, "Passwords do not match."
    
    # Check if username already exists
    if db.query(User).filter(User.username == username).first():
        return False, "Username already exists."

    # Generate hashed password and secret key
    hashed_password = get_password_hash(password)
    secret_key = generate_secret_key(user_password=password)

    # Add new user to database
    new_user = User(username=username, hashed_password=hashed_password, hashed_secret_key=get_secret_key_hash(secret_key))
    db.add(new_user)
    db.commit()

    return True, secret_key.decode()



def generate_secret_key(user_password: str) -> bytes:
    password_bytes = user_password.encode()  # Convert string to bytes
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,  # Fernet keys are 32 bytes
            salt=salt,
            iterations=100000,
            backend=default_backend())
    key = base64.urlsafe_b64encode(kdf.derive(password_bytes))
    
    return key

def generate_static_key(specific_string: str) -> bytes:
    # Convert the specific string to bytes
    specific_string = specific_string.encode()

    # Choose a salt (you can generate it randomly or use a fixed value)
    salt = b'MySaltValue'  # Change this to a random value if needed

    # Generate the key using PBKDF2HMAC
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,  # 32 bytes key length
        salt=salt,
        iterations=100000,  # You can adjust the number of iterations as needed
        backend=default_backend()
    )

    # Derive the key
    key = base64.urlsafe_b64encode(kdf.derive(specific_string))

    return key

def encrypt_data(data, key):
    cipher_suite = Fernet(key)
    encrypted_data = cipher_suite.encrypt(data.encode())
    return encrypted_data

def decrypt_data(encrypted_data, key):
    cipher_suite = Fernet(key)
    decrypted_data = cipher_suite.decrypt(encrypted_data).decode()
    return decrypted_data







