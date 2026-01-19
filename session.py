class Session:
    def __init__(self):
        self.user_id = None

    def set(self, user_id):
        self.user_id = user_id

session = Session() # Session is a singleton; there can only be one session per instance of the application.
