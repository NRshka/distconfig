from typing import Union, Optional
import bcrypt
import base64

from server.database import AbstractDatabase


class User:
    def __init__(
        self,
        username: str,
        id: Union[int, str],
        is_auth: bool,
        is_active: bool
    ):
        self.username = username
        self.id = id
        self.is_authenticated = is_auth
        self.is_acive = is_active
        self.is_anonymous = False

    def get_id(self):
        return str(self.id)


class UsersManager:
    def __init__(self, database: AbstractDatabase, salt: bytes):
        self.db = database
        self.salt = salt

    def authorize(self, username: str, password: str) -> Optional[User]:
        password_ = password.encode('utf-8')
        password_hash = bcrypt.hashpw(password_, self.salt)
        password_hash = base64.b64encode(password_hash)
        password_hash_str = password_hash.decode('utf-8')

        records = self.db.get_users(username, password_hash_str)

        if records:
            return User(username, records[0].get('id'), True, True)

        return None
