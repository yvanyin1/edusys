from contextlib import contextmanager
import os
import mysql.connector
from dotenv import load_dotenv


class DBUtils(object):

    def __init__(self):
        # Load environment variables
        load_dotenv(dotenv_path='../../.env_test')
        self.__db_name = os.getenv("DB_NAME", "education_management_test")

    def get_db_name(self):
        return self.__db_name

    def get_connection(self):
        try:
            return mysql.connector.connect(
                host=os.getenv("DB_HOST"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                database=self.__db_name,
            )
        except mysql.connector.Error as err:
            print(f"Database connection failed: {err}")
            raise


# if __name__ == "__main__":
#     db = DBUtil()
#     print(db.get_connection())
#     print(db.get_db_name())
