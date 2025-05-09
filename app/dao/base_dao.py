from abc import abstractmethod
from app.utils.db_utils import DBUtils

class BaseDAO(object):

    def __init__(self, table_name: str, connection=None):
        self._connection = connection or DBUtils().get_connection()
        self._table_name = table_name

    def get_connection(self):
        return self._connection

    def count_rows(self):
        connection = None
        cursor = None
        try:
            connection = DBUtils().get_connection()
            cursor = connection.cursor()
            cursor.execute(f'SELECT COUNT(*) FROM {self._table_name}')
            return cursor.fetchone()[0]
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def get_all_rows(self):
        connection = None
        cursor = None
        try:
            connection = DBUtils().get_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(f"SELECT * FROM {self._table_name}")
            return cursor.fetchall()
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def get_max_element_in_column(self, column_name):
        connection = None
        cursor = None
        try:
            connection = DBUtils().get_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(f"SELECT MAX({column_name}) FROM {self._table_name}")
            return cursor.fetchone()[f"MAX({column_name})"]
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def get_varchar_max_length(self, column_name, schema_name):
        connection = None
        cursor = None
        try:
            connection = DBUtils().get_connection()
            cursor = connection.cursor()
            query = """
                    SELECT CHARACTER_MAXIMUM_LENGTH
                    FROM INFORMATION_SCHEMA.COLUMNS
                    WHERE TABLE_SCHEMA = %s
                      AND TABLE_NAME = %s
                      AND COLUMN_NAME = %s
                    """
            cursor.execute(query, (schema_name, self._table_name, column_name))
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                raise ValueError(
                    f"No such column '{column_name}' in table '{self._table_name}' in schema '{schema_name}'"
                )
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def get_rows_by_column_value(self, value, column_name: str) -> list[dict]:
        connection = None
        cursor = None
        try:
            connection = DBUtils().get_connection()
            cursor = connection.cursor(dictionary=True)
            query = f"SELECT * FROM {self._table_name} WHERE {column_name} = %s"
            cursor.execute(query, (value,))
            return cursor.fetchall()
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    @staticmethod
    @abstractmethod
    def build_entity_object(row: dict):
        """Convert a DB row into an entity object."""
        pass
