from flask import session
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
from database.database import Database


class LogIn:
    def __init__(self, username, password):
        self.username = str(username)
        self.password = str(password)
        self.database_password = None
        self.key = None

    def Password_Check(self):
        if self.database_password == self.password:
            return True
        else:
            return False

    @staticmethod
    def Decryption(key, message):
        encoded_message = message.encode()
        binary_message = key.decrypt(encoded_message)
        decoded_message = binary_message.decode()
        return decoded_message

    def Password_Decode(self):
        key_object = Fernet(self.key)
        self.database_password = self.Decryption(key_object, self.database_password)
        return self.Password_Check()

    def Key_Maker(self):
        key_base = self.username[::-1]
        encoded_key_base = key_base.encode()
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'\xcfz\xfc\xdcF\xc1d\xc1\xb4\xfa5%\xe7\xa5\x14\x16',
            iterations=100000,
            backend=default_backend()
        )
        self.key = base64.urlsafe_b64encode(kdf.derive(encoded_key_base))
        return self.Password_Decode()

    def Check_Username(self):
        command = {'Username': self.username}
        username_result = Database.find_one('user_data', command)
        if username_result is None:
            return False
        else:
            self.database_password = username_result['Password']
            return self.Key_Maker()

    def User_session_create(self):
        user_data = Database.find_one('user_data', {'Username': self.username})
        session['name'] = user_data['Name']
        session['mobile'] = user_data['Mobile']
        session['username'] = self.username
        session['balance'] = user_data['Balance']
        session['key'] = self.key
