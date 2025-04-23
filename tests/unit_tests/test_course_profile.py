import pytest
import mysql
from mysql.connector.errors import IntegrityError, DataError


def test_course_profile_count(db_connection):
    """Test that the number of course profiles is exactly 3"""
    cursor = db_connection.cursor()
    cursor.execute('SELECT COUNT(*) FROM course_profile')
    count = cursor.fetchone()[0]
    assert count == 3
    cursor.close()


def test_create_course_profile_distinct(db_connection):
    """Test that adding a course profile makes the number of rows increment by 1 and check for presence of row"""
    cursor = db_connection.cursor()

    # Fetch and count distinct course_ids before insertion
    cursor.execute('SELECT * FROM course_profile')
    before_insert = cursor.fetchall()
    initial_count = len(before_insert)

    # Insert a new course
    sql = "INSERT INTO course_profile (course_name, course_code) VALUES (%s, %s)"
    values = ("Numerical Computing", "COMP 350")
    cursor.execute(sql, values)
    db_connection.commit()

    # Fetch and count again after insertion
    cursor.execute('SELECT * FROM course_profile')
    rows = cursor.fetchall()
    new_count = len(rows)
    assert new_count == initial_count + 1

    # Check if new row is here
    new_row = rows[-1]
    assert new_row[0] == 4 and new_row[1] == "Numerical Computing" and new_row[2] == "COMP 350"

    cursor.close()


def test_insert_duplicate_course_code_raises_error(db_connection):
    """Test that inserting a duplicate course_code raises an IntegrityError"""
    cursor = db_connection.cursor()

    # Attempt to insert a duplicate course_code
    sql = "INSERT INTO course_profile (course_name, course_code, course_desc, target_audience) VALUES (%s, %s, %s, %s)"
    values = ("Some Course", "COMP 250", "Some Description", 1)

    with pytest.raises(IntegrityError):
        cursor.execute(sql, values)
        db_connection.commit()

    cursor.close()


def test_insert_null_course_name_raises_error(db_connection):
    """Test that inserting a duplicate course_code raises an IntegrityError"""
    cursor = db_connection.cursor()

    # Attempt to insert a duplicate course_code
    sql = "INSERT INTO course_profile (course_name, course_code, course_desc, target_audience) VALUES (%s, %s, %s, %s)"
    values = (None, "COMP 249", "Some Description", 1)

    with pytest.raises(IntegrityError):
        cursor.execute(sql, values)
        db_connection.commit()

    cursor.close()


def test_insert_long_course_name_raises_error(db_connection):
    """Test that inserting a duplicate course_code raises an IntegrityError"""
    cursor = db_connection.cursor()

    cursor.execute("""
                   SELECT CHARACTER_MAXIMUM_LENGTH
                   FROM INFORMATION_SCHEMA.COLUMNS
                   WHERE TABLE_SCHEMA = %s
                     AND TABLE_NAME = %s
                     AND COLUMN_NAME = %s
                   """, ("education_management_test", "course_profile", "course_name"))
    max_course_name_length = cursor.fetchone()[0]

    # Attempt to insert a duplicate course_code
    sql = "INSERT INTO course_profile (course_name, course_code, course_desc, target_audience) VALUES (%s, %s, %s, %s)"
    long_course_name = (max_course_name_length + 1) * "A"  # course_name is of type VARCHAR(50)
    values = (long_course_name, "COMP 249", "Some Description", 1)

    with pytest.raises(DataError):
        cursor.execute(sql, values)
        db_connection.commit()

    cursor.close()


# # CREATE
# cursor = connection.cursor()
# sql = "INSERT INTO course_profile (course_name, course_code) VALUES (%s, %s)"
# values = ("Numerical Computing", "COMP 350")
# cursor.execute(sql, values)
# connection.commit()
# print(f"{cursor.rowcount} record inserted.")
#
# # READ
# cursor = connection.cursor()
# cursor.execute("SELECT * FROM course_profile")
# results = cursor.fetchall()
# for row in results:
#     print(row)
#
# # UPDATE
# cursor = connection.cursor()
# sql = "UPDATE course_profile SET course_desc = %s WHERE course_name = %s"
# values = ("MATLAB operations", "Numerical Computing")
# cursor.execute(sql, values)
# connection.commit()
# print(f"{cursor.rowcount} record(s) updated.")
#
# cursor = connection.cursor()
# cursor.execute("SELECT * FROM course_profile")
# results = cursor.fetchall()
# for row in results:
#     print(row)
#
# # DELETE
# cursor = connection.cursor()
# sql = "DELETE FROM course_profile WHERE course_name = %s"
# values = ("Numerical Computing",)
# cursor.execute(sql, values)
# connection.commit()
# print(f"{cursor.rowcount} record(s) deleted.")
#
# cursor = connection.cursor()
# cursor.execute("SELECT * FROM course_profile")
# results = cursor.fetchall()
# for row in results:
#     print(row)
#
# cursor.close()