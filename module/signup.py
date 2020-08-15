from flask import sessions
import random
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
from database.database import Database


class SignUp:
    def __init__(self, name, mobile, username, password, confirm_password):
        self.name = str(name)
        self.mobile = str(mobile)
        self.username = str(username)
        self.password = str(password)
        self.confirm_password = str(confirm_password)
        self.key = None
        self.balance = 0

    def json(self):
        return{
            'Name': self.name,
            'Mobile': self.mobile,
            'Username': self.username,
            'Password': self.password,
            'Balance': self.balance
        }

    def Upload_to_database(self):
        upload_to_database_command = self.json()
        upload_to_database_result = Database.insert_one("user_data", upload_to_database_command)
        if upload_to_database_result:
            print(upload_to_database_result)
            return False
        else:
            return True

    @staticmethod
    def Encryption(key, message):
        encoded_message = message.encode()
        binary_message = key.encrypt(encoded_message)
        decoded_message = binary_message.decode()
        return decoded_message

    def Encode_Data(self):
        key_object = Fernet(self.key)
        self.name = self.Encryption(key_object, self.name)
        self.mobile = self.Encryption(key_object, str(self.mobile))
        self.password = self.Encryption(key_object, self.password)
        self.balance = self.Encryption(key_object, str(self.balance))
        return self.Upload_to_database()

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
        return self.Encode_Data()

    def Mobile_Verification(self):
        generate_otp = int(random.randint(100000, 999999))
        # Send otp using sms
        print("OTP:" + str(generate_otp))
        # ==================
        enter_otp = int(input("\n\nEnter OTP:"))
        if enter_otp != generate_otp:
            print("OTP not Matched...!")
            return False
        else:
            return self.Key_Maker()

    def Username_Repeat(self):
        username_result = Database.find_one("user_data", {'Username': self.username})
        if username_result is None:
            return self.Mobile_Verification()
        else:
            print("Username already exits, Choose different one...!")
            return False

    def Check_Retype_Password(self):
        if self.password != self.confirm_password:
            print("Retyped Password not matched...!")
            return False
        else:
            return self.Username_Repeat()
