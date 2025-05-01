import mysql.connector
import os
from datetime import datetime

class StudentUtils(object):

    @staticmethod
    def generate_unique_student_id():
        """Generates a unique student ID in the format YYYYMMNNNN."""
        current_date = datetime.now()
        prefix = current_date.strftime("%Y%m")  # e.g., "202504"

        # Connect to DB
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        cursor = connection.cursor()

        # Get all student_ids starting with this prefix
        cursor.execute("""
                       SELECT student_id
                       FROM student_profile
                       WHERE student_id LIKE %s
                       ORDER BY student_id DESC LIMIT 1
                       """, (prefix + '%',))

        result = cursor.fetchone()
        if result:
            last_id = int(result[0])
            new_id = str(last_id + 1)
        else:
            new_id = prefix + "0001"

        cursor.close()
        connection.close()

        return new_id