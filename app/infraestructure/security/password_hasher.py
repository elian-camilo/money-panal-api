from pwdlib import PasswordHash
from app.application.interfaces.password_hasher import PasswordHasherInterface

class PasswordHasher(PasswordHasherInterface):
    def __init__(self):
        self.password_hash = PasswordHash.recommended()
        
        DUMMY_PASSWORD = self.password_hash.hash("dummy_password_crazy_long_to_avoid_collisions")

    def hash_password(self, password: str) -> str:
        return self.password_hash.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.password_hash.verify(plain_password, hashed_password)