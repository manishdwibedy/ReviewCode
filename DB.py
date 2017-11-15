from pymongo import MongoClient
import json
import ast

class DB(object):

    def __init__(self):
        client = MongoClient('mongodb://admin:qwerty123@ds163745.mlab.com:63745/review-code', 27017)
        self.db = client['review-code']
        self.users = self.db.users
        self.questions = self.db.questions
        self.reviews = self.db.reviews

    def addUser(self, user):
        json1 = json.dumps(user, default=lambda o: o.__dict__)
        response = self.users.insert_one(ast.literal_eval(json1))
        return response

    def getUsers(self):
        users = list(self.db.users.find())
        return users

    def addQuestion(self, question):
        json1 = json.dumps(question, default=lambda o: o.__dict__)
        response = self.questions.insert_one(ast.literal_eval(json1))
        return response

    def getQuestions(self):
        questions = list(self.db.questions.find())
        return questions

    def addReview(self, review):
        json1 = json.dumps(review, default=lambda o: o.__dict__)
        response = self.reviews.insert_one(ast.literal_eval(json1))
        return response

    def getReviews(self):
        reviews = list(self.db.reviews.find())
        return reviews

