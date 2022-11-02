class LoginExistsException(Exception):
    def __init__(self, login: str):
        self.login = login

