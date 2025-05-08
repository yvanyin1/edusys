from abc import abstractmethod

class BaseDAO(object):

    def __init__(self, connection, table_name: str):
        self._connection = connection
        self._table_name = table_name

    def get_connection(self):
        return self._connection

    def count_rows(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(f'SELECT COUNT(*) FROM {self._table_name}')
        return cursor.fetchone()[0]

    def get_all_rows(self):
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM {self._table_name}")
        return cursor.fetchall()

    def get_max_element_in_column(self, column_name):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT MAX({column_name}) FROM {self._table_name}")
        return cursor.fetchone()[0]

    def get_varchar_max_length(self, column_name, schema_name):
        conn = self.get_connection()
        cursor = conn.cursor()
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
            raise ValueError(f"No such column '{column_name}' in table '{self._table_name}' in schema '{schema_name}'")

    def get_rows_by_column_value(self, value, column_name: str) -> list[dict]:
        query = f"SELECT * FROM {self._table_name} WHERE {column_name} = %s"
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, (value,))
        return cursor.fetchall()

    @staticmethod
    @abstractmethod
    def build_entity_object(row: dict):
        """Convert a DB row into an entity object."""
        pass