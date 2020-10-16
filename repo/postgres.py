from .base import AbstractRepository, ConnectionAPI
from typing import Optional, Sequence, Any
from .models import User
import psycopg2


class PostgresRepository(AbstractRepository):
    """ Specific Repository to handle a postgres database server as repo for the application"""

    def __init__(self, repository_url: str):
        super().__init__(repository_url)
        self.connection = None
        self.connection_class_api = PostgresConnectionAPI

    def _connect(self):
        """ Build a connection to the """
        # 1. Step get params out of the url
        connection_param_dict = self.parse_postgres_url(self.repo_url)
        # 2. Step: Build a connection with psycopg2
        # 3. Step :set self_connection to the build connection
        # 3.Step: return the connection
        return self.connection

    @staticmethod
    def parse_postgres_url(repo_url):
        """ Parse the params necessary to connect to postgres database"""
        # 1.Step: Parse url
        # 2 Step: Save it in correct form
        # connection_param_dict = {user: "", pw: "", host: "", db_name: ""}
        # return connection_param_dict
        return repo_url

    def can_connect(self) -> bool:
        """ Try to build a connection. It's a validation, if true the repo can be initialized,
         if not an error or Dummy repo is needed"""

        # build a connection and execute SELECT name FROM sqlite_master
        return True

    def initialize(self) -> bool:
        """Initialize the repository, if needed."""
        # 1.Step: Try to Connect
        # if not connection:
        #   return False

        # 2. Step: Try to get table schema for every table which does not exist. Create it
        # cursor = connection.cursor()
        # try:
        #     cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
        #     tables = {row[0] for row in cursor.fetchall()}
        # if "users" not in tables:
        #     cursor.execute("""
        # CREATE TABLE users(
        #     ...)
        # """)

        return True

    def create(self) -> ConnectionAPI:
        """ Create a ConnectionAPI object with an open connection"""
        return self.connection_class_api(self._connect())


class PostgresConnectionAPI(ConnectionAPI):

    def __init__(self, connection):
        self._connection = connection

    def close(self, success: bool):
        """Close the connection."""
        if success:
            self._execute("COMMIT")
        if self._connection is not None:
            self._connection.close()
        self._connection = None

    def _execute(
            self, sql: str, values: Sequence[Any] = ()):
        """Execute a SQL command."""
        if self._connection is None:
            raise TypeError("SQLite connection is None")
        return self._connection.execute(sql, values)

    def get_user_by_ident(self, ident: str):
        """Get a User by his identification"""
        # 1. First step: Execute query with _execute
        # cursor = self._execute("SELECT ...")   # cursor is self._connection.execute(sql, values)
        # Save results in Model
        # row = cursor.fetchone()  # psychopg interface here
        # cursor.close()
        return User  # User(row[0], ...)
