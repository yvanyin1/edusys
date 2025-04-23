# Fixtures and DB Setup

import pytest
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path='.env_test')

@pytest.fixture(scope="session")
def db_connection():
    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
    )
    yield connection
    connection.close()


@pytest.fixture(autouse=True)
def reset_database(db_connection):
    cursor = db_connection.cursor()

    # Empty the table before each test to ensure no leftover data
    cursor.execute("TRUNCATE TABLE course_profile;")

    # Insert the initial rows (reset the table to its initial state)
    sql_insert = """
                 INSERT INTO course_profile(course_name, course_code, course_desc, target_audience, duration_in_weeks, \
                                            credit_hours, profile_status)
                 VALUES ('Introduction to Computer Science', 'COMP 250', \
                         'Searching/sorting algorithms, data structures', 2, 15, 3.0, 1), \
                        ('Theory of Computation', 'COMP 330', NULL, 2, 12, 3.0, 1), \
                        ('Sampling Theory and Applications', 'MATH 525', 'Horvitz-Thompson estimator', 1, 10, 3.0, 1); \
                 """

    cursor.execute(sql_insert)

    # Commit changes and close the cursor
    db_connection.commit()
    cursor.close()
