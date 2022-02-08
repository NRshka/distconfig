from typing import Union, Optional
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
        port: Optional[Union[str, int]]
    ):
        print('\tHOST:', host)
        print('\tLogind:', login)
        print('\tPassword:', password)
        super().__init__(host, login, password, database, port)
        self.loop = asyncio.get_event_loop()
        self.postgres_conn = self.loop.run_until_complete(self.connect())

    async def connect(self):
        return await asyncpg.connect(
            host=self.host,
            user=self.login,
            password=self.password,
            database=self.database_name,
            port=self.port
        )

    def execute_sql(self, sql_command: str):
        return self.loop.run_until_complete(self.execute_sql_(sql_command))

    async def execute_sql_(self, sql_command: str):
        async with self.postgres_conn.transaction():
            answer = await self.postgres_conn.execute(sql_command)

        return answer

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
                username
            )
        )

        return users
