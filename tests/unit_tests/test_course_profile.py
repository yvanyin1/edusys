import pytest
from app.models.course_profile import CourseProfile
from app.enums.audience_type import AudienceType
from app.enums.profile_status import ProfileStatus
from app.dao.course_profile_dao import CourseProfileDAO
from mysql.connector.errors import IntegrityError, DataError, DatabaseError


def test_course_profile_count(db_connection):
    """Test that the number of course profiles is exactly 3"""
    dao = CourseProfileDAO(db_connection)
    count = dao.count_course_profiles()
    assert count == 3


def test_create_course_profile_distinct(db_connection):
    """Test that adding a course profile makes the number of rows increment by 1 and check for presence of row"""
    dao = CourseProfileDAO(db_connection)
    initial_count_rows = dao.count_course_profiles()
    initial_last_row_id = dao.get_max_course_id()
    last_row_id = dao.create_course_profile(CourseProfile(-1, "Numerical Computing", "COMP 350",
                                            "", AudienceType.ADULT, 13,
                                            3.0, ProfileStatus.ACTIVE))  # -1 is a dummy course_id

    assert last_row_id == initial_last_row_id + 1
    assert dao.count_course_profiles() == initial_count_rows + 1

    rows = dao.get_rows()
    # Check if new row is here
    new_row = rows[-1]

    assert new_row[0] == 4 and new_row[1] == "Numerical Computing" and new_row[2] == "COMP 350"


def test_insert_duplicate_course_code_raises_error(db_connection):
    """Test that inserting a duplicate course_code raises an IntegrityError"""

    dao = CourseProfileDAO(db_connection)

    # A row with course_code = "COMP 250" already exists in the table
    duplicate_course = CourseProfile(
        course_id=None,
        course_name="Duplicate Course",
        course_code="COMP 250",  # same code triggers UNIQUE constraint
        course_desc="Some Description",
        target_audience=AudienceType.ADULT,
        duration_in_weeks=None,
        credit_hours=None,
        profile_status=ProfileStatus.ACTIVE
    )

    with pytest.raises(IntegrityError):
        dao.create_course_profile(duplicate_course)



def test_insert_null_course_name_raises_error(db_connection):
    """Test that inserting a NULL course_name raises an IntegrityError"""
    dao = CourseProfileDAO(db_connection)

    # A row with course_code = "COMP 250" already exists in the table
    null_name_course = CourseProfile(
        course_id=1,
        course_name=None,
        course_code="COMP 249",  # same code triggers UNIQUE constraint
        course_desc="Some Description",
        target_audience=AudienceType.ADULT,
        duration_in_weeks=None,
        credit_hours=None,
        profile_status=ProfileStatus.ACTIVE
    )

    with pytest.raises(IntegrityError):
        dao.create_course_profile(null_name_course)


def test_insert_long_course_name_raises_error(db_connection):
    """Test that inserting a course_course name that exceeds character limit raises a DataError"""
    dao = CourseProfileDAO(db_connection)
    max_course_name_length = dao.get_varchar_max_length("course_name",
                                                        "education_management_test")

    null_name_course = CourseProfile(
        course_id=1,
        course_name=(max_course_name_length + 1) * "A",  # Overly long course name
        course_code="AAAA 444",
        course_desc="Some Description",
        target_audience=AudienceType.ADULT,
        duration_in_weeks=None,
        credit_hours=None,
        profile_status=ProfileStatus.ACTIVE
    )

    with pytest.raises(DataError):
        dao.create_course_profile(null_name_course)


def test_insert_invalid_enum_value_raises_error(db_connection):
    """Test that inserting an out-of-range enum-like value raises an IntegrityError"""
    cursor = db_connection.cursor()

    # Valid values for target_audience are 1 and 2 — we try inserting 3
    sql = """
    INSERT INTO course_profile (course_name, course_code, course_desc, target_audience)
    VALUES (%s, %s, %s, %s)
    """
    values = ("Valid Name", "COMP 999", "Testing enum constraint", 3)

    with pytest.raises(DatabaseError):
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