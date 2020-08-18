from flask import session
from cryptography.fernet import Fernet


class Profile:
    def __init__(self):
        if session is not None:
            self.username = session['username']
            self.key = session['key']
            self.name = session['name']
            self.mobile = session['mobile']
            self.balance = session['balance']
        else:
            self.username = None

    @staticmethod
    def logout():
        session['username'] = None
        session['key'] = None
        session['name'] = None
        session['mobile'] = None
        session['balance'] = None

    @staticmethod
    def Decryption(key, message):
        encoded_message = message.encode()
        binary_message = key.decrypt(encoded_message)
        decoded_message = binary_message.decode()
        return decoded_message

    def Data_Decode(self):
        key_object = Fernet(self.key)
        session['name'] = self.name = Profile.Decryption(key_object, self.name)
        session['mobile'] = self.mobile = Profile.Decryption(key_object, self.mobile)
        session['balance'] = self.balance = Profile.Decryption(key_object, self.balance)
        return self
