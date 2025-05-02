from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import mysql.connector
import os
from datetime import datetime

from app.dao.scheduled_class_session_dao import ScheduledClassSessionDAO
from app.enums.session_change_type import SessionChangeType
from app.enums.session_type import SessionType
from app.models.course_profile import CourseProfile
from app.models.scheduled_class_session import ScheduledClassSession
from app.models.student_profile import StudentProfile
from app.models.teacher_profile import TeacherProfile
from app.models.class_schedule import ClassSchedule

from app.enums.audience_type import AudienceType
from app.enums.profile_status import ProfileStatus
from app.enums.enrollment_status import EnrollmentStatus
from app.enums.guardian_status import GuardianStatus
from app.enums.class_type import ClassType
from app.enums.day_of_week import DayOfWeek
from app.enums.flag import Flag

from app.dao.course_profile_dao import CourseProfileDAO
from app.dao.student_profile_dao import StudentProfileDAO
from app.dao.teacher_profile_dao import TeacherProfileDAO
from app.dao.class_schedule_dao import ClassScheduleDAO
from app.dao.classroom_location_dao import ClassroomLocationDAO
from app.dao.semester_dao import SemesterDAO

from app.utils.student_utils import StudentUtils

audience_type_map = {
    "General Audience": AudienceType.GENERAL_AUDIENCE,
    "Adult": AudienceType.ADULT,
    "Youth": AudienceType.YOUTH
}

profile_status_map = {
    "Active": ProfileStatus.ACTIVE,
    "Inactive": ProfileStatus.INACTIVE
}

enrollment_status_map = {
    "Inactive": EnrollmentStatus.INACTIVE,
    "Enrolled": EnrollmentStatus.ENROLLED,
    "Graduated": EnrollmentStatus.GRADUATED
}

guardian_status_map = {
    "No Guardian": GuardianStatus.NO_GUARDIAN,
    "Has Guardian": GuardianStatus.HAS_GUARDIAN
}

class_type_map = {
    "Regular": ClassType.REGULAR,
    "Recreational": ClassType.RECREATIONAL,
    "One To One": ClassType.ONE_TO_ONE,
    "Workshop": ClassType.WORKSHOP,
    "Intensive": ClassType.INTENSIVE,
}

load_dotenv(dotenv_path='.env_test')

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__)))
template_dir = os.path.join(basedir, 'templates')

app = Flask(__name__, template_folder=template_dir)
app.secret_key = os.getenv("SECRET_KEY", "dev")

# Configure SQLAlchemy with MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = (f"mysql+mysqlconnector://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
                                         + f"{os.getenv('DB_HOST')}/education_management_test")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


def get_connection():
    return mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database="education_management_test",
        )

# TODO for testing purposes
def load_initial_data():
    """Function to load initial data from SQL query."""
    try:
        # Connect to the database using MySQL connector
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database="education_management_test",
        )
        cursor = connection.cursor()

        # Insert course data
        cursor.execute("DROP TABLE IF EXISTS course_profile")
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
                    (3, 2025, '2025-09-08', '2025-12-19', '2025-09-06 23:59:59', '2025-10-15 23:59:59'),
                    (3, 2026, '2025-01-05', '2025-04-24', '2025-01-03 23:59:59', '2025-02-15 23:59:59');"""
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
        cursor.execute("DROP TABLE IF EXISTS class_schedule")
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
                                                (1, 2, 1, 3, "DFA for one person"), \
                                                (1, 3, 30, 1, "Statistics in a medium-sized class");"""
        cursor.execute(sql_insert_class_schedules)

        # Insert scheduled class sessions data
        cursor.execute("""DROP TABLE IF EXISTS scheduled_class_session""")
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

        connection.commit()
        cursor.close()
        connection.close()

    except Exception as e:
        print(f"Error loading initial data: {e}")

# TODO for testing purposes
load_initial_data()


@app.route('/')
def index():
    return redirect(url_for("home"))

@app.route('/home')
def home():
    return render_template("home_page.html", username="dluo")


@app.route('/course-management')
def course_management():
    return render_template("course_management.html", username="dluo")


@app.route('/student-management')
def student_management():
    return render_template("student_management.html", username="dluo")


@app.route('/create-course-profile')
def create_course_profile():
    return render_template("create_course_profile_form.html", username="dluo")


@app.route('/course-profile-created', methods=['POST'])
def course_profile_created():

    course_name = request.form['course_name']
    course_code = request.form['course_code']
    course_desc = request.form['course_desc']
    target_audience_string = request.form['target_audience']
    target_audience = audience_type_map[target_audience_string]
    duration_in_weeks = request.form['duration_in_weeks']
    prerequisites = request.form['prerequisites']  # will handle that logic later
    corequisites = request.form['corequisites']
    credit_hours = request.form['credit_hours']
    profile_status_string = request.form['profile_status']
    profile_status = profile_status_map[profile_status_string]

    # Add course profile to database
    connection = get_connection()
    dao = CourseProfileDAO(connection)

    form_data = {
        'course_name': course_name,
        'course_code': course_code,
        'course_desc': course_desc,
        'target_audience': target_audience_string,
        'duration_in_weeks': duration_in_weeks,
        'prerequisites': prerequisites,
        'corequisites': corequisites,
        'credit_hours': credit_hours,
        'profile_status': profile_status_string
    }

    # Check if course name or code already exists
    if dao.get_course_by_name(course_name):
        flash(f"A course with the name '{course_name}' already exists.", 'warning')
        return render_template("create_course_profile_form.html", form_data=form_data, username="dluo")

    if dao.get_course_by_code(course_code):
        flash(f"A course with the code '{course_code}' already exists.", 'warning')
        return render_template("create_course_profile_form.html", form_data=form_data, username="dluo")


    new_course_profile = CourseProfile(0, course_name, course_code,
                                            course_desc, target_audience, int(duration_in_weeks),
                                            float(credit_hours), profile_status)
    dao.create_course_profile(new_course_profile)

    course_data = {
        'course_name': course_name,
        'course_code': course_code,
        'course_desc': course_desc,
        'target_audience': target_audience_string,
        'duration_in_weeks': duration_in_weeks,
        'prerequisites': prerequisites,
        'corequisites': corequisites,
        'credit_hours': credit_hours,
        'profile_status': profile_status_string
    }

    return render_template("create_course_profile_success.html", course=course_data, username="dluo")


@app.route('/read-course-profiles')
def read_course_profiles():
    filter_column = request.args.get('filter_column')
    filter_value = request.args.get('filter_value')

    valid_columns = {'course_id', 'course_code', 'course_name', 'profile_status'}

    if filter_column and filter_column not in valid_columns:
        return "Invalid filter column", 400

    try:
        connection = get_connection()
        dao = CourseProfileDAO(connection)
        courses = dao.read_course_profiles(filter_column, filter_value)

        return render_template(
            "read_course_profiles.html",
            courses=courses,
            filter_column=filter_column,
            filter_value=filter_value,
            username="dluo"
        )
    except Exception as e:
        return f"Error fetching courses: {e}"

@app.route('/update-course-profile/search', methods=["GET"])
def update_course_profile_search():
    return render_template("update_course_profile_search.html", username="dluo")


@app.route('/update-course-profile/edit-course', methods=['GET'])
def edit_course_profile():
    course_name_or_code = request.args.get('course_name_or_code')

    connection = get_connection()
    dao = CourseProfileDAO(connection)
    course_profile = dao.get_course_by_name(course_name_or_code) if dao.get_course_by_name(
        course_name_or_code) else dao.get_course_by_code(course_name_or_code)

    enum_to_string = {
        course_profile.get_target_audience(): AudienceType(course_profile.get_target_audience()).name.title().replace("_", " "),
        course_profile.get_profile_status(): ProfileStatus(course_profile.get_profile_status()).name.title()
    }

    return render_template("update_course_profile_edit.html",
                           course=course_profile, enum_to_string=enum_to_string, username="dluo")


@app.route('/update-course-profile/success', methods=['POST'])
def update_course_profile_success():
    course_id = request.form['course_id']
    course_name = request.form['course_name']
    course_code = request.form['course_code']
    course_desc = request.form['course_desc']
    target_audience_string = request.form['target_audience']
    target_audience = audience_type_map[target_audience_string]
    duration_in_weeks = request.form['duration_in_weeks']
    prerequisites = request.form['prerequisites']  # will handle that logic later
    corequisites = request.form['corequisites']
    credit_hours = request.form['credit_hours']
    profile_status_string = request.form['profile_status']
    profile_status = profile_status_map[profile_status_string]

    # Update course profile in database
    connection = get_connection()
    dao = CourseProfileDAO(connection)
    dao.update_course_profile(CourseProfile(course_id, course_name, course_code,
                                            course_desc, target_audience, int(duration_in_weeks),
                                            float(credit_hours), profile_status))

    course_data = {
        'course_name': course_name,
        'course_code': course_code,
        'course_desc': course_desc,
        'target_audience': target_audience_string,
        'duration_in_weeks': duration_in_weeks,
        'prerequisites': prerequisites,
        'corequisites': corequisites,
        'credit_hours': credit_hours,
        'profile_status': profile_status_string
    }

    return render_template("update_course_profile_success.html", course=course_data, username="dluo")


@app.route('/delete-course-profile/search', methods=['GET'])
def delete_course_profile_search():
    return render_template("delete_course_profile_search.html", username="dluo")


@app.route('/delete-course-profile/success', methods=['POST'])
def delete_course_profile_success():
    course_name_or_code = request.form["course_name_or_code"]

    connection = get_connection()
    dao = CourseProfileDAO(connection)
    course_profile = dao.get_course_by_name(course_name_or_code) if dao.get_course_by_name(
        course_name_or_code) else dao.get_course_by_code(course_name_or_code)
    dao.delete_course_profile(course_profile.get_course_id())
    course_data = {
        'course_name': course_profile.get_name(),
        'course_code': course_profile.get_code(),
    }
    return render_template("delete_course_profile_success.html", course=course_data, username="dluo")


@app.route('/create-student-profile')
def create_student_profile():
    return render_template("create_student_profile_form.html", username="dluo")


@app.route('/student-profile-created', methods=['POST'])
def student_profile_created():
    # Extract form data
    student_id = StudentUtils.generate_unique_student_id()
    first_name = request.form['first_name']
    middle_name = request.form.get('middle_name', '')
    last_name = request.form['last_name']
    birth_date = request.form.get('birth_date') or None
    phone_number = request.form.get('phone_number', '')
    email_address = request.form['email_address']
    home_address = request.form.get('home_address', '')
    registration_date = request.form.get('registration_date') or datetime.today().date().isoformat()  # YYYY-MM-DD for today
    enrollment_status_string = request.form['enrollment_status']
    enrollment_status = enrollment_status_map[enrollment_status_string]
    guardian_status_string = request.form['guardian_status']
    guardian_status = guardian_status_map[guardian_status_string]
    profile_status_string = request.form['profile_status']
    profile_status = profile_status_map[profile_status_string]

    form_data = {
        'first_name': first_name,
        'middle_name': middle_name,
        'last_name': last_name,
        'birth_date': birth_date,
        'phone_number': phone_number,
        'email_address': email_address,
        'home_address': home_address,
        'registration_date': registration_date,
        'enrollment_status': enrollment_status_string,
        'guardian_status': guardian_status_string,
        'profile_status': profile_status_string
    }

    # Connect to DB
    connection = get_connection()
    dao = StudentProfileDAO(connection)

    # Check for duplicate email
    if dao.get_student_by_email(email_address):
        flash(f"A student with the email '{email_address}' already exists.", 'warning')
        return render_template("create_student_profile_form.html", form_data=form_data, username="dluo")

    # Create student profile
    new_student = StudentProfile(
        0, first_name, middle_name, last_name,
        birth_date, phone_number, email_address,
        home_address, registration_date,
        enrollment_status, guardian_status, profile_status
    )
    dao.create_student_profile(new_student)

    # Pass student data to success template
    student_data = {
        'student_id': student_id,
        'first_name': first_name,
        'middle_name': middle_name,
        'last_name': last_name,
        'birth_date': birth_date,
        'phone_number': phone_number,
        'email_address': email_address,
        'home_address': home_address,
        'registration_date': registration_date,
        'enrollment_status': enrollment_status_string,
        'guardian_status': guardian_status_string,
        'profile_status': profile_status_string
    }

    return render_template("create_student_profile_success.html", student=student_data, username="dluo")


@app.route('/read_student_profiles')
def read_student_profiles():
    filter_column = request.args.get('filter_column')
    filter_value = request.args.get('filter_value')

    valid_columns = {'student_id', 'first_name', 'last_name', 'profile_status'}

    if filter_column and filter_column not in valid_columns:
        return "Invalid filter column", 400

    try:
        connection = get_connection()
        dao = StudentProfileDAO(connection)
        students = dao.read_student_profiles(filter_column, filter_value)

        return render_template(
            "read_student_profiles.html",
            students=students,
            filter_column=filter_column,
            filter_value=filter_value,
            username="dluo"
        )
    except Exception as e:
        return f"Error fetching courses: {e}"


@app.route('/update-student-profile/search', methods=["GET"])
def update_student_profile_search():
    return render_template("update_student_profile_search.html", username="dluo")


@app.route('/update-student-profile/edit-student', methods=['GET'])
def edit_student_profile():
    student_id = int(request.args.get('student_id'))

    connection = get_connection()
    dao = StudentProfileDAO(connection)
    student_profile = dao.get_student_by_id(student_id)
    enum_to_string = {
        student_profile.get_enrollment_status(): EnrollmentStatus(student_profile.get_enrollment_status()).name.title(),
        student_profile.get_guardian_status(): GuardianStatus(student_profile.get_guardian_status()).name.title().replace("_", " "),
        student_profile.get_profile_status(): ProfileStatus(student_profile.get_profile_status()).name.title()
    }

    return render_template("update_student_profile_edit.html",
                           student=student_profile, enum_to_string=enum_to_string, username="dluo")


@app.route('/update-student-profile/success', methods=['POST'])
def update_student_profile_success():
    student_id = request.form['student_id']
    first_name = request.form['first_name']
    middle_name = request.form['middle_name']
    last_name = request.form['last_name']
    birth_date = request.form['birth_date']
    phone_number = request.form['phone_number']
    email_address = request.form['email_address']
    home_address = request.form['home_address']
    registration_date = request.form['registration_date']
    enrollment_status_string = request.form['enrollment_status']
    guardian_status_string = request.form['guardian_status']
    profile_status_string = request.form['profile_status']

    enrollment_status = enrollment_status_map[enrollment_status_string]
    guardian_status = guardian_status_map[guardian_status_string]
    profile_status = profile_status_map[profile_status_string]

    connection = get_connection()
    dao = StudentProfileDAO(connection)
    dao.update_student_profile(StudentProfile(student_id, first_name, middle_name, last_name, birth_date,
                                              phone_number, email_address, home_address, registration_date,
                                              enrollment_status, guardian_status, profile_status))

    student_data = {
        'student_id': student_id,
        'first_name': first_name,
        'middle_name': middle_name,
        'last_name': last_name,
        'birth_date': birth_date,
        'phone_number': phone_number,
        'email_address': email_address,
        'home_address': home_address,
        'registration_date': registration_date,
        'enrollment_status': enrollment_status_string,
        'guardian_status': guardian_status_string,
        'profile_status': profile_status_string
    }

    return render_template("update_student_profile_success.html", student=student_data, username="dluo")


@app.route('/teacher-management')
def teacher_management():
    return render_template("teacher_management.html", username="dluo")


@app.route('/read-teacher-profiles')
def read_teacher_profiles():
    filter_column = request.args.get('filter_column')
    filter_value = request.args.get('filter_value')

    valid_columns = {'teacher_id', 'first_name', 'last_name', 'employment_status', 'teacher_role', 'profile_status'}

    if filter_column and filter_column not in valid_columns:
        return "Invalid filter column", 400

    try:
        connection = get_connection()
        dao = TeacherProfileDAO(connection)
        teachers = dao.read_teacher_profiles(filter_column, filter_value)

        return render_template(
            "read_teacher_profiles.html",
            teachers=teachers,
            filter_column=filter_column,
            filter_value=filter_value,
            username="dluo"
        )
    except Exception as e:
        return f"Error fetching teachers: {e}"


@app.route('/class-management')
def class_management():
    return render_template("class_management.html", username="dluo")


@app.route('/class-management/create-class-schedule')
def create_class_schedule():
    connection = get_connection()
    course_profile_dao = CourseProfileDAO(connection)
    active_courses = course_profile_dao.read_course_profiles("profile_status", 1)
    semester_dao = SemesterDAO(connection)
    semesters = semester_dao.read_semester_data()
    class_types = list(ClassType)
    return render_template("create_class_schedule.html", active_courses=active_courses,
                           semesters=semesters, class_types=class_types, username="dluo")


@app.route('/class-management/create-class-schedule-success', methods=['POST'])
def class_schedule_created():
    connection = get_connection()
    course_profile = CourseProfileDAO(connection).get_course_by_id(int(request.form['course_id']))
    semester = SemesterDAO(connection).get_semester_by_id(int(request.form['semester_id']))
    class_capacity = request.form['class_capacity']
    class_type_string = request.form['class_type']
    class_desc = request.form['class_desc']

    # Convert to correct types
    class_type = class_type_map[class_type_string]  # assuming this map exists like profile_status_map

    connection = get_connection()
    dao = ClassScheduleDAO(connection)

    form_data = {
        'course_name': course_profile.get_name(),
        'semester_name': semester.get_name(),
        'class_capacity': class_capacity,
        'class_type': class_type_string,
        'class_desc': class_desc
    }

    # (Optional) Any custom validation you want here
    if int(class_capacity) <= 0:
        flash("Class capacity must be a positive number.", 'warning')
        return render_template("create_class_schedule.html", form_data=form_data, username="dluo", semesters=..., active_courses=..., classroom_locations=...)

    new_schedule = ClassSchedule(
        schedule_id=0,
        course_id=course_profile.get_course_id(),
        semester_id=semester.get_semester_id(),
        class_capacity=int(class_capacity),
        class_type=class_type,
        class_desc=class_desc
    )

    dao.create_class_schedule(new_schedule)

    return render_template("create_class_schedule_success.html", class_schedule=form_data, username="dluo")


@app.route('/read-class-schedules')
def read_class_schedules():
    class_schedules = ClassScheduleDAO(get_connection()).read_class_schedules()
    return "<br>".join([str(schedule) for schedule in class_schedules])


@app.route('/create-scheduled-class-session')
def create_scheduled_class_session():
    connection = get_connection()
    class_schedule_dao = ClassScheduleDAO(connection)
    class_schedules_dict = class_schedule_dao.read_class_schedules()
    course_profiles = [
        class_schedule_dao.get_course_profile_by_schedule_id(schedule["schedule_id"])
        for schedule in class_schedules_dict
    ]
    class_schedule_names = [{"schedule_id": schedule["schedule_id"], "course_code": course.get_code(), "course_name": course.get_name()}
                            for (schedule, course) in zip(class_schedules_dict, course_profiles)]

    classroom_location_dao = ClassroomLocationDAO(connection)
    classroom_locations = classroom_location_dao.read_classroom_location_data()

    days = list(DayOfWeek)
    session_types = list(SessionType)
    session_change_types = list(SessionChangeType)
    flags = list(Flag)

    return render_template("create_scheduled_class_session.html",
                           class_schedule_names=class_schedule_names,
                           classroom_locations=classroom_locations,
                           days=days, session_types=session_types, session_change_types=session_change_types,
                           flags=flags, username="dluo")


@app.route('/create-scheduled-class-session-success', methods=["POST"])
def scheduled_class_session_created():
    try:
        schedule_id = int(request.form["schedule_id"])
        location_id = int(request.form["location_id"])
        day_of_week = DayOfWeek(int(request.form["day_of_week"]))
        start_time = request.form["start_time"]
        end_time = request.form["end_time"]
        session_type = SessionType[request.form["session_type"]]
        scheduled_date = request.form["scheduled_date"]
        seq_no = int(request.form["seq_no"])
        session_change_type_str = request.form.get("session_change_type")
        session_change_type = SessionChangeType[session_change_type_str] if session_change_type_str else None
        flag = Flag(int(request.form["flag"]))

        session = ScheduledClassSession(
            session_id=None,
            schedule_id=schedule_id,
            location_id=location_id,
            day_of_week=day_of_week,
            start_time=start_time,
            end_time=end_time,
            session_type=session_type,
            scheduled_date=scheduled_date,
            seq_no=seq_no,
            session_change_type=session_change_type,
            flag=flag,
        )

        ScheduledClassSessionDAO(get_connection()).create_class_session(session)
        flash("Scheduled session created successfully!", "success")
        return redirect(url_for("create_scheduled_class_session"))

    except Exception as e:
        flash(f"Failed to create session: {str(e)}", "warning")

        # Pull fresh values for re-rendering form
        connection = get_connection()
        class_schedule_dao = ClassScheduleDAO(connection)
        class_schedules_dict = class_schedule_dao.read_class_schedules()
        course_profiles = [
            class_schedule_dao.get_course_profile_by_schedule_id(schedule["schedule_id"])
            for schedule in class_schedules_dict
        ]
        class_schedule_names = [{"schedule_id": schedule["schedule_id"], "course_code": course.get_code(), "course_name": course.get_name()}
                                for (schedule, course) in zip(class_schedules_dict, course_profiles)]

        classroom_location_dao = ClassroomLocationDAO(connection)
        classroom_locations = classroom_location_dao.read_classroom_location_data()

        days = list(DayOfWeek)
        session_types = list(SessionType)
        session_change_types = list(SessionChangeType)
        flags = list(Flag)

        form_data = request.form.to_dict()

        return render_template("create_scheduled_class_session.html",
                               class_schedule_names=class_schedule_names,
                               classroom_locations=classroom_locations,
                               days=days,
                               session_types=session_types,
                               session_change_types=session_change_types,
                               flags=flags,
                               form_data=form_data,
                               username="dluo")


if __name__ == '__main__':
    app.run(debug=True)
