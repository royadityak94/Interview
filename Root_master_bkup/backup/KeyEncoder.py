from cryptography.fernet import Fernet
import random
import string

def generate_random_salt(size=None):
    if not size:
        size = random.randint(8, 40)
    possibilities = string.ascii_letters + string.digits
    return ''.join([random.choice(possibilities)
        for _ in range(size)])

class KeyEncoder:
    def __init__(self, salt=None):
        if not salt:
            salt = generate_random_salt()
        self.crypto = Fernet(Fernet.generate_key().decode('utf-8') + salt)
    def encrypt(self, key):
        return self.crypto.encrypt(key.encode())
    def decrypt(self, key):
        return self.crypto.decrypt(key).decode()
