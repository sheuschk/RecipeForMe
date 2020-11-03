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
        try:
            con = psycopg2.connect(host=self.repo_url['host'],
                                   user=self.repo_url['user'],
                                   password=self.repo_url['pw'],
                                   database=self.repo_url['database'])
            return con

        except psycopg2.OperationalError:
            return self.connection

        except Exception:
            # 3. Step :set self_connection to the build connection
            # 3.Step: return the connection
            return self.connection

    def can_connect(self) -> bool:
        """ Try to build a connection. It's a validation, if true the repo can be initialized,
         if not an error or Dummy repo is needed"""
        con = self._connect()
        if con:
            if getattr(con, 'closed') == 0:
                return True
            else:
                return False
        return False

    def initialize(self) -> bool:
        """Initialize the repository, if needed."""
        con = self._connect()
        if not con:
            return False
        cursor = con.cursor()
        try:
            cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' ")

            tables = {row[0] for row in cursor.fetchall()}
            if "users" not in tables:
                # enter sql schema to initialise the application
                pass
        finally:
            cursor.close()
            con.commit()
        return True

    def create(self) -> ConnectionAPI:
        """ Create a ConnectionAPI object with an open connection"""
        return self.connection_class_api(self._connect())


class PostgresConnectionAPI(ConnectionAPI):

    def __init__(self, connection):
        self._connection = connection

    def close(self):
        """Close the connection."""
        if self._connection is not None:
            self._connection.close()
        self._connection = None

    def _execute_one(self, sql_query: str, values: Sequence[Any] = ()):
        """Execute a SQL command."""
        if self._connection is None:
            raise TypeError("SQLite connection is None")

        cur = self._connection.cursor()
        cur.execute(sql_query, values)
        row = cur.fetchone()
        cur.close()
        return row

    def _execute(self, sql_query: str, values: Sequence[Any] = ()):
        cur = self._connection.cursor()
        cur.execute(sql_query, values)
        cur.close()
        self._connection.commit()

    def get_user_by_ident(self, ident: str):
        """Get a User by his identification"""
        # 1. First step: Execute query with _execute
        # cursor = self._execute("SELECT ...")   # cursor is self._connection.execute(sql, values)
        # Save results in Model
        # row = cursor.fetchone()  # psychopg interface here
        # cursor.close()
        return User  # User(row[0], ...)
