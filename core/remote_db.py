import os
from dotenv import load_dotenv
from sshtunnel import SSHTunnelForwarder
import pymysql
from typing import List, Dict, Any, Optional
from contextlib import contextmanager

load_dotenv()


class RemoteMySQL:
    def __init__(self):
        self.ssh_host = os.getenv("SSH_HOST")
        self.ssh_port = int(os.getenv("SSH_PORT"))
        self.ssh_user = os.getenv("SSH_USER")
        self.ssh_password = os.getenv("SSH_PASSWORD")

        self.sql_host = os.getenv("SQL_HOST")
        self.sql_port = int(os.getenv("SQL_PORT"))
        self.sql_user = os.getenv("SQL_USER")
        self.sql_password = os.getenv("SQL_PASSWORD")
        self.sql_db = os.getenv("SQL_DB")

    @contextmanager
    def _get_connection(self):
        tunnel = None
        conn = None

        try:
            tunnel = SSHTunnelForwarder(
                (self.ssh_host, self.ssh_port),
                ssh_username=self.ssh_user,
                ssh_password=self.ssh_password,
                remote_bind_address=(self.sql_host, self.sql_port),
            )
            tunnel.start()

            conn = pymysql.connect(
                host="127.0.0.1",
                port=tunnel.local_bind_port,
                user=self.sql_user,
                password=self.sql_password,
                database=self.sql_db,
                cursorclass=pymysql.cursors.DictCursor,
                charset="utf8mb4",
            )

            yield conn

        finally:
            if conn:
                try:
                    conn.close()
                except:
                    pass

            if tunnel:
                try:
                    tunnel.stop()
                except:
                    pass

    def query(self, sql: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, params or ())
                return cursor.fetchall()

    def query_one(self, sql: str, params: Optional[tuple] = None) -> Optional[Dict[str, Any]]:
        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, params or ())
                return cursor.fetchone()

    def execute(self, sql: str, params: Optional[tuple] = None) -> int:
        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                result = cursor.execute(sql, params or ())
                conn.commit()
                return result
