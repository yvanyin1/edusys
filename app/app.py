from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import mysql.connector
import os
from datetime import datetime

from app.models.course_profile import CourseProfile
from app.models.student_profile import StudentProfile

from app.enums.audience_type import AudienceType
from app.enums.profile_status import ProfileStatus
from app.enums.enrollment_status import EnrollmentStatus
from app.enums.guardian_status import GuardianStatus

from app.dao.course_profile_dao import CourseProfileDAO
from app.dao.student_profile_dao import StudentProfileDAO
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
        cursor.execute("DROP TABLE IF EXISTS student_profile")
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
            INSERT INTO student_profile(first_name, middle_name, last_name, birth_date,
                phone_number, email_address, home_address, subject_expertise, employment_status, teacher_role, profile_status),
            VALUES ('Albert', '', 'Einstein', '1879-03-14', '5143141879', 'emc2@gmail.com', '123 Relativity Street', 'Physics, Science', 1, 1, 1),
                    ('Alan', 'Mathison', 'Turing', '1912-06-23', '5146231912', 'turing@gmail.com', '468 Fox Street', 'Computer Science', 3, 1, 0),
                    ('Harald', '', 'Cramer', '1893-09-25', '5149251893', 'haraldcramer@gmail.com', '100 Gothenburg Street', 'Statistics', 2, 2, 1);
            """
        cursor.execute(sql_insert_teachers)

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
    return "Teacher!"


if __name__ == '__main__':
    app.run(debug=True)
