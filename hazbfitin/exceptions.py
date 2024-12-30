"""
Файл со всеми исключениями
"""


class BaseAesException(Exception):
    """
    Базовый exception for all AES exceptions.
    """
    pass


class MessageCorrupt(BaseAesException):
    """
    Exception raised when a message is corrupt.
    """
    pass


class NicknameAlreadyTaken(BaseAesException):
    """
        Exception raised when a Nickname is taken.
    """
    pass
