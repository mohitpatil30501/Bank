from database.database import Database
import datetime
import time


class History:
    def __init__(self, username, process, amount, description):
        self.username = username
        self.transaction = None
        self.process = process
        self.amount = amount
        self.description = description
        self.time = datetime.datetime.now()
        self.history = None

    def json(self):
        return {
            'TransactionId': self.transaction,
            'Process': self.process,
            'Amount': self.amount,
            'Description': self.description,
            'Time': self.time
        }

    def Generate_Transaction_Id(self):
        user_database_id = Database.find_one("user_data", {'Username': self.username})
        user_id = str(user_database_id['_id']) + str(int(time.time()))
        return user_id

    def Upload_History(self):
        Database.update_one('user_data', {'Username': self.username}, {'$set': {'History': self.history}})

    def Retrieve_History(self):
        history_data = Database.find_one('user_data', {'Username': self.username})
        return history_data['History']

    def Process_History(self):
        self.history = self.Retrieve_History()
        self.history.append(self.json())
        self.Upload_History()

    def Id_Generate(self):
        self.transaction = self.Generate_Transaction_Id()
        self.Process_History()
