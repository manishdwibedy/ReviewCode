import time

class Review(object):
    def __init__(self):
        self.question_id = "question_id"
        self.user_id = "user_id"
        self.review_text = ""
        self.timestamp = time.time()