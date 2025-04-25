import pytest
from app.models.course_profile import CourseProfile
from app.enums.audience_type import AudienceType
from app.enums.profile_status import ProfileStatus
from app.dao.course_profile_dao import CourseProfileDAO
from mysql.connector.errors import IntegrityError, DataError, DatabaseError


def test_course_profile_count(db_connection):
    """Test that the number of course profiles in initial table is exactly 3"""
    dao = CourseProfileDAO(db_connection)
    count = dao.count_course_profiles()
    assert count == 3


def test_create_course_profile(db_connection):
    """Test that adding a course profile makes the number of rows increment by 1 and check for presence of row"""
    dao = CourseProfileDAO(db_connection)
    initial_count_rows = dao.count_course_profiles()
    initial_last_row_id = dao.get_max_course_id()
    new_course_profile = CourseProfile(
        course_id=-1,  # -1 is a dummy course_id
        course_name="Numerical Computing",
        course_code="COMP 350",
        course_desc="",
        target_audience=AudienceType.ADULT,
        duration_in_weeks=13,
        credit_hours=3.0,
        profile_status=ProfileStatus.ACTIVE)
    last_row_id = dao.create_course_profile(new_course_profile)

    assert last_row_id == initial_last_row_id + 1
    assert dao.count_course_profiles() == initial_count_rows + 1

    rows = dao.get_rows()
    # Check if new row is here
    new_row = rows[-1]

    assert new_row[0] == 4 and new_row[1] == "Numerical Computing" and new_row[2] == "COMP 350"


def test_create_duplicate_course_code_raises_error(db_connection):
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


def test_create_null_course_name_raises_error(db_connection):
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


def test_create_long_course_name_raises_error(db_connection):
    """Test that inserting a course_course name that exceeds character limit raises a DataError"""
    dao = CourseProfileDAO(db_connection)
    max_course_name_length = dao.get_varchar_max_length("course_name",
                                                        "education_management_test")

    long_name_course = CourseProfile(
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
        dao.create_course_profile(long_name_course)


def test_read_course_profiles(db_connection):
    """Test reading course profiles"""
    dao = CourseProfileDAO(db_connection)
    courses = dao.read_course_profiles()
    assert [course["course_name"]
            for course in courses] == ["Introduction to Computer Science",
                                       "Theory of Computation", "Sampling Theory and Applications"]
    assert [course["course_code"] for course in courses] == ["COMP 250", "COMP 330", "MATH 525"]


def test_read_course_profiles_one_course_subject(db_connection):
    dao = CourseProfileDAO(db_connection)
    courses = dao.read_course_profiles(filter_column="course_code", filter_value="COMP")
    assert [course["course_name"]
            for course in courses] == ["Introduction to Computer Science", "Theory of Computation"]
    assert [course["course_code"] for course in courses] == ["COMP 250", "COMP 330"]


def test_update_course_profile(db_connection):
    """Test that updating a course profile does not change the number of rows and check for modified row values"""
    dao = CourseProfileDAO(db_connection)
    initial_count_rows = dao.count_course_profiles()
    course_profile_to_update = dao.get_course_by_name("Introduction to Computer Science")
    course_id = course_profile_to_update.get_course_id()
    course_profile_updated = CourseProfile(
        course_id=course_id,
        course_name="Introduction to Computer Science",
        course_code="COMP 250",
        course_desc="Searching/sorting algorithms, data structures, time complexity",
        target_audience=AudienceType.YOUTH,
        duration_in_weeks=19,
        credit_hours=3.0,
        profile_status=ProfileStatus.ACTIVE
    )
    dao.update_course_profile(course_profile_updated)
    assert dao.count_course_profiles() == initial_count_rows  # should remain unchanged
    updated_course_profile = dao.get_course_by_id(course_id)  # fetch the updated row
    assert updated_course_profile.get_course_id() == course_id  # should remain unchanged
    assert updated_course_profile.get_name() == "Introduction to Computer Science"
    assert updated_course_profile.get_code() == "COMP 250"
    assert updated_course_profile.get_description() == "Searching/sorting algorithms, data structures, time complexity"
    assert updated_course_profile.get_target_audience() == AudienceType.YOUTH
    assert updated_course_profile.get_duration_in_weeks() == 19
    assert updated_course_profile.get_credit_hours() == 3.0
    assert updated_course_profile.get_profile_status() == ProfileStatus.ACTIVE

def test_update_nonexistent_course_raises_error(db_connection):
    """Test that updating a non-existent course raises a ValueError"""
    dao = CourseProfileDAO(db_connection)
    nonexistent_course_id = 999
    assert dao.get_course_by_id(nonexistent_course_id) is None

    nonexistent_course_profile = CourseProfile(
        course_id=nonexistent_course_id,
        course_name="Unknown",
        course_code="COMP 999",
        course_desc="Some Description",
        target_audience=AudienceType.YOUTH,
        duration_in_weeks=19,
        credit_hours=3.0,
        profile_status=ProfileStatus.ACTIVE
    )

    with pytest.raises(ValueError):
        dao.update_course_profile(nonexistent_course_profile)

def test_update_course_name_too_long_raises_error(db_connection):
    """Test that updating a course name with an overly long name raises a ValueError"""
    dao = CourseProfileDAO(db_connection)
    max_course_name_length = dao.get_varchar_max_length("course_name",
                                                        "education_management_test")
    course_profile_to_update = dao.get_course_by_name("Introduction to Computer Science")
    course_id = course_profile_to_update.get_course_id()

    long_name_course = CourseProfile(
        course_id=course_id,
        course_name=(max_course_name_length + 1) * "A",  # Overly long course name
        course_code="COMP 250",
        course_desc="Some Description",
        target_audience=AudienceType.ADULT,
        duration_in_weeks=None,
        credit_hours=None,
        profile_status=ProfileStatus.ACTIVE
    )

    with pytest.raises(DataError):
        dao.create_course_profile(long_name_course)

def test_delete_course_profile(db_connection):
    """Test that deleting a course profile decrements the number of rows and check for absence of row"""
    dao = CourseProfileDAO(db_connection)
    initial_count_rows = dao.count_course_profiles()
    course_profile_to_delete = dao.get_course_by_name("Sampling Theory and Applications")
    course_id = course_profile_to_delete.get_course_id()
    dao.delete_course_profile(course_id)
    assert dao.count_course_profiles() == initial_count_rows - 1
    assert dao.get_course_by_name("Sampling Theory and Applications") is None

def test_delete_nonexistent_course_raises_error(db_connection):
    """Test that deleting a nonexistent course profile raises a ValueError"""
    dao = CourseProfileDAO(db_connection)
    nonexistent_course_id = 999
    assert dao.get_course_by_id(nonexistent_course_id) is None
    with pytest.raises(ValueError):
        dao.delete_course_profile(nonexistent_course_id)
