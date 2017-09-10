# User class for use with Flask Login

class User(object):
    def __init__(self, email):
        self.email = email
    
    def get_id(self):
        return self.email

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True
    