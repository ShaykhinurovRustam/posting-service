from core.exceptions import CustomException


class PasswordDoesNotMatchException(CustomException):
    code = 401
    error_code = "USER__PASSWORD_DOES_NOT_MATCH"
    message = "Password does not match"


class DuplicateEmailOrNicknameException(CustomException):
    code = 400
    error_code = "USER__DUPLICATE_EMAIL_OR_NICKNAME"
    message = "Duplicate email or nickname"


class UserNotFoundException(CustomException):
    code = 404
    error_code = "USER__NOT_FOUND"
    message = "User not found"


class UnauthorizedException(CustomException):
    code = 401
    error_code = "UNAUTHORIZED"
    message = ""