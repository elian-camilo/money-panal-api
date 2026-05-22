from pwdlib import PasswordHash
from dotenv import load_dotenv
import os
from app.domain.repositories.password_hasher import PasswordHasherInterface

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class PasswordHasher(PasswordHasherInterface):
    def __init__(self):
        self.password_hash = PasswordHash.recommended()

        DUMMY_PASSWORD = self.password_hash.hash("dummy_password_crazy_long_to_avoid_collisions")

    def hash_password(self, password: str) -> str:
        return self.password_hash.hash(password)
    
    def verify_password(self, plain_password, hashed_password):
        return self.password_hash.verify(plain_password, hashed_password)