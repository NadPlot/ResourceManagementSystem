class PhoneExistsException(Exception):
    def __init__(self, phone: int):
        self.phone = phone

