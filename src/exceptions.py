from werkzeug.exceptions import HTTPException


class CustomErrorException(HTTPException):
    def __init__(self, message, code):
        self.message = message
        self.code = code
        super().__init__(message, code)
