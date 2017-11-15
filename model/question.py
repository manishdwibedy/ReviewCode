import time

class Question(object):
    def __init__(self):
        self._id = {
            '$oid': ''
        }
        self.author_id = "sample_id"
        self.author_username = "Sample User"
        self.language = ""
        self.language_mode = ""
        self.question_title = ""
        self.question_code = ""
        self.timestamp = time.time()