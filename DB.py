from pymongo import MongoClient, ReturnDocument
from bson import ObjectId
import json
import ast
import arrow

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
        json_string = json.dumps(question, default=lambda o: o.__dict__)
        json_dict = ast.literal_eval(json_string)
        response = self.questions.insert_one(json_dict)
        return response

    def getQuestions(self):
        questions = list(self.db.questions.find())

        for question in questions:
            date = arrow.get(question['timestamp'])
            question['time'] = date.humanize()
        return questions

    def getQuestion(self, id):
        question = list(self.db.questions.find({
            "_id": ObjectId(id)
            # "author_username" : "Sample User"
        }))

        date = arrow.get(question[0]['timestamp'])
        question[0]['time'] = date.humanize()
        return question

    def addReview(self, review):

        json_string = json.dumps(review, default=lambda o: o.__dict__)
        json_dict = ast.literal_eval(json_string)
        response = self.reviews.insert_one(json_dict)

        return response

    def getReviews(self, question_id):
        reviews = list(self.db.reviews.find({
            'question_id': question_id
        }))
        for review in reviews:
            date = arrow.get(review['timestamp'])
            review['time'] = date.humanize()

        return reviews

