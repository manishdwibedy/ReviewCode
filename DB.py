from pymongo import MongoClient
import json
import ast

class DB(object):

    def __init__(self):
        client = MongoClient('mongodb://admin:qwerty123@ds163745.mlab.com:63745/review-code', 27017)
        self.db = client['review-code']
        self.users = self.db.users
        self.codes = self.db.codes

    def addUser(self, user):
        json1 = json.dumps(user, default=lambda o: o.__dict__)
        users = self.users.insert_one(ast.literal_eval(json1))


    def getUsers(self):
        users = list(self.db.users.find())
        users


    def getCodes(self):
        pass