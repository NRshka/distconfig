from typing import Union, Optional
import os


def read_db_config_from_envs():
    database_login = os.getenv("DATABASE_LOGIN")
    assert database_login, RuntimeError("No DATABASE_LOGIN is provided")

    database_password = os.getenv("DATABASE_PASSWORD")
    assert database_password, RuntimeError("No DATABASE_PASSWORD is provided")

    database_host = os.getenv("DATABASE_HOST")
    assert database_host, RuntimeError("No DATABASE_HOST is provided")

    database_name = os.getenv("DATABASE_NAME")
    assert database_name

    database_port = os.getenv("DATABASE_PORT")

    if database_port:
        database_port = int(database_port)

    return (
        database_host,
        database_login,
        database_password,
        database_name,
        database_port,
    )


class AbstractDatabase:
    def __init__(
        self,
        host: str,
        login: str,
        password: str,
        database: str,
        port: Optional[Union[str, int]],
    ):
        self.host = host
        self.login = login
        self.password = password
        self.database_name = database
        self.port = port

    def execute_sql(self, sql_command: str):
        raise NotImplementedError("AbstractDatabase")

    def authenticate_user(self, username: str, password: str) -> Optional[int]:
        raise NotImplementedError("AbstractDatabase")

    def get_users(self, username: str, password_hash: str) -> list:
        raise NotImplementedError("AbstractDatabase")

    def register_user(self, username: str, email: str, password_hash: str):
        raise NotImplementedError("AbstractDatabase")
