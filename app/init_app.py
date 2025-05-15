from dotenv import load_dotenv
import mysql.connector
import os
from datetime import date, timedelta

from app.enums.class_enrollment_status import ClassEnrollmentStatus
from app.enums.session_type import SessionType

from app.models.scheduled_class_session import ScheduledClassSession
from app.models.student_enrollment_details import StudentEnrollmentDetails

from app.enums.day_of_week import DayOfWeek
from app.enums.flag import Flag

from app.dao.student_enrollment_details_dao import StudentEnrollmentDetailsDAO
from app.dao.scheduled_class_session_dao import ScheduledClassSessionDAO


# Load environment variables
load_dotenv(dotenv_path='../.env_test')

# Validate required environment variables early
required_env_vars = ["DB_HOST", "DB_USER", "DB_PASSWORD"]
missing = [var for var in required_env_vars if not os.getenv(var)]
if missing:
    raise EnvironmentError(f"Missing required environment variables: {', '.join(missing)}")

DB_NAME = os.getenv("DB_NAME", "education_management_test")

def get_connection():
    try:
        return mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=DB_NAME,
        )
    except mysql.connector.Error as err:
        print(f"Database connection failed: {err}")
        raise


# TODO for testing purposes
def load_initial_data():
    """Function to load initial data from SQL query."""
    try:
        # Connect to the database using MySQL connector
        connection = get_connection()
        cursor = connection.cursor()

        # Drop existing tables
        cursor.execute("DROP TABLE IF EXISTS student_enrollment_details")
        cursor.execute("DROP TABLE IF EXISTS scheduled_class_session")
        cursor.execute("DROP TABLE IF EXISTS class_schedule")
        cursor.execute("DROP TABLE IF EXISTS course_profile")

        # Insert course data
        cursor.execute("""CREATE TABLE course_profile (
            course_id INT NOT NULL AUTO_INCREMENT,  -- for some reason adding NOT NULL removes an error
            course_name VARCHAR(50) NOT NULL UNIQUE,
            course_code VARCHAR(10) NOT NULL UNIQUE,
            course_desc TEXT,
            target_audience TINYINT DEFAULT 1 CHECK (target_audience BETWEEN 1 AND 3),
            duration_in_weeks TINYINT,
            credit_hours FLOAT,
            profile_status TINYINT NOT NULL DEFAULT 0 CHECK (profile_status IN (0, 1)),
            PRIMARY KEY (course_id)
        );""")
        sql_insert_courses = """
            INSERT INTO course_profile(course_name, course_code, course_desc, target_audience, duration_in_weeks, credit_hours, profile_status)
            VALUES ('Introduction to Computer Science', 'COMP 250', 'Searching/sorting algorithms, data structures', 2, 15, 3.0, 1),
                   ('Theory of Computation', 'COMP 330', NULL, 2, 12, 3.0, 1),
                   ('Sampling Theory and Applications', 'MATH 525', 'Horvitz-Thompson estimator', 1, 10, 3.0, 1);
        """
        cursor.execute(sql_insert_courses)

        # Insert student data
        cursor.execute("DROP TABLE IF EXISTS student_profile")
        cursor.execute("""CREATE TABLE student_profile (
            student_id VARCHAR(10) NOT NULL UNIQUE,
            first_name VARCHAR(30) NOT NULL,
            middle_name VARCHAR(30),
            last_name VARCHAR(30) NOT NULL,
            birth_date DATE,
            phone_number VARCHAR(15),
            email_address VARCHAR(120) NOT NULL UNIQUE,
            home_address VARCHAR(255),
            registration_date DATE,
            enrollment_status TINYINT NOT NULL DEFAULT 0 CHECK (enrollment_status BETWEEN 0 AND 2),
            guardian_status TINYINT(1) NOT NULL DEFAULT 0 CHECK (guardian_status IN (0, 1)),
            profile_status TINYINT NOT NULL DEFAULT 0 CHECK (profile_status IN (0, 1)),
            PRIMARY KEY (student_id)
        );""")
        sql_insert_students = """
            INSERT INTO student_profile(student_id, first_name, middle_name, last_name, birth_date, phone_number, email_address, home_address, registration_date, enrollment_status, guardian_status, profile_status)
            VALUES ('2025050001', 'Daniel', 'Ziyang', 'Luo', '1998-12-10', '5141234567', 'daniel.luo@mail.mcgill.ca', '123 rue Street', '2025-03-27', 1, 0, 1),
                    ('2025050002', 'Brian', 'Harold', 'May', '1947-07-19', '4381234567', 'brianmay@gmail.com', '1975 rue Queen', '2024-10-31', 0, 0, 0),
                    ('2025050003', 'Farrokh', '', 'Bulsara', '1946-09-05', '4501234567', 'freddiemercury@gmail.com', '1975 rue Bohemian', '2024-01-31', 1, 1, 1);"""
        cursor.execute(sql_insert_students)

        # Insert teacher data
        cursor.execute("DROP TABLE IF EXISTS teacher_profile")
        cursor.execute("""CREATE TABLE teacher_profile (
            teacher_id INT AUTO_INCREMENT,
            first_name VARCHAR(30) NOT NULL,
            middle_name VARCHAR(30),
            last_name VARCHAR(30) NOT NULL,
            birth_date DATE,
            phone_number VARCHAR(15),
            email_address VARCHAR(120) NOT NULL UNIQUE,
            home_address VARCHAR(255),
            subject_expertise VARCHAR(100) NOT NULL,
            employment_status TINYINT NOT NULL DEFAULT 0 CHECK (employment_status BETWEEN 0 AND 3),
            teacher_role TINYINT NOT NULL DEFAULT 1 CHECK (teacher_role IN (1, 2)),
            profile_status TINYINT NOT NULL DEFAULT 0 CHECK (profile_status IN (0, 1)),
            PRIMARY KEY (teacher_id)
        );""")
        sql_insert_teachers= """
            INSERT INTO teacher_profile(first_name, middle_name, last_name, birth_date,
                phone_number, email_address, home_address, subject_expertise, employment_status, teacher_role, profile_status)
            VALUES ('Albert', '', 'Einstein', '1879-03-14', '5143141879', 'emc2@gmail.com', '123 Relativity Street', 'Physics, Science', 1, 1, 1),
                    ('Alan', 'Mathison', 'Turing', '1912-06-23', '5146231912', 'turing@gmail.com', '468 Fox Street', 'Computer Science', 3, 1, 0),
                    ('Harald', '', 'Cramer', '1893-09-25', '5149251893', 'haraldcramer@gmail.com', '100 Gothenburg Street', 'Statistics', 2, 2, 1);
            """
        cursor.execute(sql_insert_teachers)

        # Insert semester data
        cursor.execute("DROP TABLE IF EXISTS semester")
        cursor.execute("""CREATE TABLE semester (
            semester_id INT AUTO_INCREMENT,
            season TINYINT NOT NULL DEFAULT 1 CHECK (season BETWEEN 1 AND 3),
            academic_year INT NOT NULL,
            start_date DATE NOT NULL,
            end_date DATE NOT NULL,
            registration_deadline DATETIME NOT NULL,
            withdrawal_deadline DATETIME NOT NULL,
            PRIMARY KEY (semester_id)
        );""")
        sql_insert_semesters = """
            INSERT INTO semester(season, academic_year, start_date, end_date, registration_deadline, withdrawal_deadline)
            VALUES (3, 2025, '2025-05-05', '2025-08-22', '2025-05-03 23:59:59', '2025-06-15 23:59:59'),
                    (1, 2025, '2025-09-08', '2025-12-19', '2025-09-06 23:59:59', '2025-10-15 23:59:59'),
                    (2, 2026, '2025-01-05', '2025-04-24', '2025-01-03 23:59:59', '2025-02-15 23:59:59');"""
        cursor.execute(sql_insert_semesters)

        # Insert classroom location data
        cursor.execute("DROP TABLE IF EXISTS classroom_location")
        cursor.execute("""CREATE TABLE classroom_location (
            location_id INT AUTO_INCREMENT,
            room_number VARCHAR(10) NOT NULL,
            building_name VARCHAR(100) NOT NULL,
            capacity INT NOT NULL,
            PRIMARY KEY (location_id)
        );""")
        sql_insert_classroom_locations = """
            INSERT INTO classroom_location(room_number, building_name, capacity)
            VALUES ("132", "Leacock", 600), ("112", "Rutherford Physics", 150), ("0132", "Trottier", 50);"""
        cursor.execute(sql_insert_classroom_locations)

        # Insert class schedule data
        cursor.execute("""CREATE TABLE class_schedule (
            schedule_id INT AUTO_INCREMENT,
            course_id INT NOT NULL,
            semester_id INT NOT NULL,
            class_capacity INT NOT NULL,
            class_type TINYINT NOT NULL DEFAULT 1 CHECK (class_type BETWEEN 1 AND 5),
            class_desc TEXT NOT NULL,
            PRIMARY KEY (schedule_id),
            FOREIGN KEY (course_id) REFERENCES course_profile(course_id),
            FOREIGN KEY (semester_id) REFERENCES semester(semester_id)
        );""")
        sql_insert_class_schedules = """
            INSERT INTO class_schedule(course_id, semester_id, class_capacity, class_type, class_desc)
                                         VALUES (1, 2, 100, 2, "Computer science in a breeze"), \
                                                (2, 2, 1, 3, "DFA for one person"), \
                                                (3, 3, 30, 1, "Statistics in a medium-sized class");"""
        cursor.execute(sql_insert_class_schedules)

        # Create scheduled class sessions table
        cursor.execute("""CREATE TABLE scheduled_class_session (
            session_id INT AUTO_INCREMENT,
            schedule_id INT NOT NULL,
            location_id INT NOT NULL,
            day_of_week TINYINT NOT NULL DEFAULT 1 CHECK (day_of_week BETWEEN 1 AND 7),
            start_time TIME NOT NULL,
            end_time TIME NOT NULL,
            session_type TINYINT NOT NULL DEFAULT 1 CHECK (session_type BETWEEN 1 AND 4),
            scheduled_date DATE NOT NULL,
            seq_no TINYINT NOT NULL,
            session_change_type TINYINT DEFAULT NULL CHECK (session_change_type IS NULL OR session_change_type BETWEEN 0 AND 3),
            flag TINYINT NOT NULL DEFAULT 1 CHECK (flag IN (0, 1)),
            PRIMARY KEY (session_id),
            FOREIGN KEY (schedule_id) REFERENCES class_schedule(schedule_id),
            FOREIGN KEY (location_id) REFERENCES classroom_location(location_id)
        );""")

        # Create student enrollment details table
        cursor.execute("""CREATE TABLE student_enrollment_details (
            enrollment_id INT AUTO_INCREMENT,
            student_id VARCHAR(10) NOT NULL,
            class_schedule_id INT NOT NULL,
            enrollment_date DATE NOT NULL,
            enrollment_status TINYINT NOT NULL DEFAULT 0 CHECK (enrollment_status BETWEEN 0 AND 3),
            PRIMARY KEY (enrollment_id),
            FOREIGN KEY (student_id) REFERENCES student_profile(student_id),
            FOREIGN KEY (class_schedule_id) REFERENCES class_schedule(schedule_id)
        );""")

        connection.commit()
        cursor.close()
        connection.close()

    except Exception as e:
        print(f"Error loading initial data: {e}")

# TODO for testing purposes
load_initial_data()


def add_initial_scheduled_class_sessions():
    cursor = None
    connection = None
    try:
        # Get the database connection
        connection = get_connection()
        cursor = connection.cursor()

        start_date = date(2025, 5, 5)
        end_date = date(2025, 8, 24)
        session_type = 1  # Assuming '1' corresponds to SessionType.LECTURE
        flag = 1  # Assuming '1' corresponds to Flag.ACTIVE
        session_change_type = None  # Assuming this is a valid value or NULL in your table

        schedule_configs = {
            1: {
                "days": [2, 4],  # 2 is Tuesday, 4 is Thursday
                "start_time": "14:30",
                "end_time": "16:00",
                "location_id": 1,
            },
            2: {
                "days": [1, 3, 5],  # 1 is Monday, 3 is Wednesday, 5 is Friday
                "start_time": "10:00",
                "end_time": "11:00",
                "location_id": 3,
            },
            3: {
                "days": [3, 5],  # 3 is Wednesday, 5 is Friday
                "start_time": "12:00",
                "end_time": "13:30",
                "location_id": 2,
            },
        }

        for schedule_id, config in schedule_configs.items():
            current_date = start_date
            seq_no = 1
            while current_date <= end_date:
                # Check if the current date is in the correct days for this schedule
                if current_date.weekday() + 1 in config["days"]:
                    # Insert the class session into the database
                    cursor.execute("""
                        INSERT INTO scheduled_class_session (
                            schedule_id, location_id, day_of_week, start_time, end_time,
                            session_type, scheduled_date, seq_no, session_change_type, flag
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        schedule_id, config["location_id"], current_date.weekday() + 1,
                        config["start_time"], config["end_time"], session_type,
                        current_date.isoformat(), seq_no, session_change_type, flag
                    ))
                    seq_no += 1
                current_date += timedelta(days=1)

            print(f"✅ Finished inserting sessions for schedule {schedule_id}")

        # Commit changes to the database
        connection.commit()

        print("🎉 All sessions inserted successfully.")
    except Exception as e:
        print(f"Error inserting scheduled class sessions: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# TODO for testing purposes
add_initial_scheduled_class_sessions()


# TODO for testing purposes
def enroll_students_in_classes_initial():
    connection = get_connection()
    dao = StudentEnrollmentDetailsDAO(connection)
    dao.create_enrollment(StudentEnrollmentDetails(0, 2025050001, 1, "2025-05-03", ClassEnrollmentStatus.ACTIVE))
    dao.create_enrollment(StudentEnrollmentDetails(0, 2025050001, 2, "2025-05-03", ClassEnrollmentStatus.ACTIVE))
    dao.create_enrollment(StudentEnrollmentDetails(0, 2025050001, 3, "2025-05-03", ClassEnrollmentStatus.ACTIVE))


# TODO for testing purposes
enroll_students_in_classes_initial()
