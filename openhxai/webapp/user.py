class User:
    """A dummy user representation for flask_login."""

    def __init__(self, id: str):
        self.id = id

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def get_id(self):
        return self.id
