from cryptography.fernet import Fernet
from flask import session

from database.database import Database
from module.history import History


class Withdraw:
    def __init__(self, amount, username, name, mobile, balance, key):
        self.deposit_amount = amount
        self.username = username
        self.name = name
        self.mobile = mobile
        self.balance = balance
        self.key = key

    def Upload_Withdraw_Data(self):
        command_1 = {'Username': self.username}
        command_2 = {'$set': {'Balance': self.balance}}
        return Database.update_one('user_data', command_1, command_2)

    @staticmethod
    def Encryption(key, message):
        encoded_message = message.encode()
        binary_message = key.encrypt(encoded_message)
        decoded_message = binary_message.decode()
        return decoded_message

    def Encrypt_Withdraw_Data(self):
        key_object = Fernet(self.key)
        self.name = self.Encryption(key_object, self.name)
        self.mobile = self.Encryption(key_object, str(self.mobile))
        self.balance = self.Encryption(key_object, str(self.balance))
        return self.Upload_Withdraw_Data()

    def Proceed_withdraw(self):
        if int(self.balance) >= int(self.deposit_amount):
            self.balance = str(int(self.balance) - int(self.deposit_amount))
            description = self.name + " withdraw Rs. " + self.deposit_amount + " Successfully."
            save_history = History(self.username, "Withdraw", self.deposit_amount, description=description)
            save_history.Id_Generate()
            return self.Encrypt_Withdraw_Data()
        else:
            return False

    @staticmethod
    def Otp_Call(payment_amount):
        session['payment_amount'] = payment_amount
        session['otp_progress'] = False
        session['process'] = 'withdraw'
