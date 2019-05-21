from flask_login import UserMixin


class User(UserMixin):

    def __init__(self, id):
        self.id = id
        self.user_name = str(id)
        self.model = None

    def __repr__(self):
        return "%s/%s" % (self.id, self.user_name)

    def set_model(self, model):
        self.model = model
        return True

    def get_model(self):
        return self.model