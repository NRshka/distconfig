from typing import Any, Tuple, Union, Optional
import asyncio
import asyncpg

from .abstract_database import AbstractDatabase


class PostgresDatabase(AbstractDatabase):
    def __init__(
        self,
        host: str,
        login: str,
        password: str,
        database: str,
        port: Optional[Union[str, int]],
    ):
        print("\tHOST:", host)
        print("\tLogind:", login)
        print("\tPassword:", password)
        super().__init__(host, login, password, database, port)
        self.loop = asyncio.get_event_loop()
        self.postgres_conn = self.loop.run_until_complete(self.connect())

    async def connect(self):
        return await asyncpg.connect(
            host=self.host,
            user=self.login,
            password=self.password,
            database=self.database_name,
            port=self.port,
        )

    def execute_sql(self, sql_command: str):
        return self.loop.run_until_complete(self.execute_sql_(sql_command))

    async def execute_sql_(self, sql_command: str, args: Tuple[Any]):
        async with self.postgres_conn.transaction():
            cursor = await self.postgres_conn.execute(sql_command, *args)

        return cursor

    def get_users(self, username: str, password_hash: str) -> list:
        """Fetch records with related provided username and password

        Args:
            username (str): string in utf-8 form
            password (str): preprocessed has of user's password in base64 form
        """
        users = self.loop.run_until_complete(
            self.postgres_conn.fetch(
                "SELECT * FROM USERS WHERE (passw = $1) AND (username = $2);",
                password_hash,
                username,
            )
        )

        return users

    async def fetch_value(self, sql_command: str, args: Tuple[Any]):
        data = await self.postgres_conn.fetchval(sql_command, *args)
        return data

    async def register_(self, username: str, email: str, password_hash: str, fullname: str, job_role: str, department: str) -> int:
        cursor = await self.execute_sql_(
            """INSERT INTO USERS(username, email, passw, full_name, job_role, department) """
            """VALUES($1, $2, $3, $4, $5, $6) RETURNING id;""",
            (username, email, password_hash, fullname, job_role, department)
        )
        id_of_new_row = cursor.fetchone()[0]

        return id_of_new_row


    def register_user(self, username: str, email: str, password_hash: str, fullname: str, job_role: str, department: str):
        # TODO check if username already exists
        new_user_id = self.loop.run_until_complete(
            self.register_(username, email, password_hash, fullname, job_role, department)
        )

        return new_user_id

    def get_username_by_id(self, user_id: int) -> Optional[str]:
        username = self.loop.run_until_complete(
            self.fetch_value(
                """SELECT username FROM USERS WHERE id=$1;""", (user_id,)
            )
        )

        return username
