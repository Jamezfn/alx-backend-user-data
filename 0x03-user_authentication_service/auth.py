from db import DB
from user import User
from sqlalchemy.exc import NoResultFound
import bcrypt

def _hash_password(password: str) -> bytes:
    """Hash a password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user"""
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_pwd = _hash_password(password)
            new_user = self._db.add_user(email, hashed_pwd)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        except InvalidRequestError:
            return False

        return bcrypt.checkpw(password.encode("utf-8"), user.hashed_password)
