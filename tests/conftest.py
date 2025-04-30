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

    with open('tests/sql_tests/create_tables.sql', 'r') as f:
        sql_script = f.read()

        # Split script by ";" and execute each statement (in case multiple statements)
    for statement in sql_script.split(';'):
        if statement.strip():
            cursor.execute(statement)

    # Insert the initial rows (reset the table to its initial state)
    sql_insert_courses = """
                 INSERT INTO course_profile(course_name, course_code, course_desc, target_audience, duration_in_weeks, \
                                            credit_hours, profile_status)
                 VALUES ('Introduction to Computer Science', 'COMP 250', \
                         'Searching/sorting algorithms, data structures', 2, 15, 3.0, 1), \
                        ('Theory of Computation', 'COMP 330', NULL, 2, 12, 3.0, 1), \
                        ('Sampling Theory and Applications', 'MATH 525', 'Horvitz-Thompson estimator', 1, 10, 3.0, 1); \
                 """
    cursor.execute(sql_insert_courses)
    sql_insert_students = """
            INSERT INTO student_profile(first_name, middle_name, last_name, birth_date, phone_number, email_address, home_address, registration_date, enrollment_status, guardian_status, profile_status)
            VALUES ('Daniel', 'Ziyang', 'Luo', '1998-12-10', '5141234567', 'daniel.luo@mail.mcgill.ca', '123 rue Street', '2025-03-27', 1, 0, 1),
                    ('Brian', 'Harold', 'May', '1947-07-19', '4381234567', 'brianmay@gmail.com', '1975 rue Queen', '2024-10-31', 0, 0, 0),
                    ('Farrokh', '', 'Bulsara', '1946-09-05', '4501234567', 'freddiemercury@gmail.com', '1975 rue Bohemian', '2024-01-31', 1, 1, 1);
                """
    cursor.execute(sql_insert_students)

    # Commit changes and close the cursor
    db_connection.commit()
    cursor.close()
