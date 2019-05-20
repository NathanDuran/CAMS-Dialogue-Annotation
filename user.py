from flask_login import UserMixin
from dialogue_model import *

class User(UserMixin):

    def __init__(self, id):
        self.id = id
        self.user_name = "user_" + str(id)
        self.model = None

    def __repr__(self):
        return "%s/%s" % (self.id, self.user_name)

    def set_model(self, model):
        self.model = model

    def get_model(self):
        return self.model