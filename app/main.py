from flask import Flask, render_template, request, flash, redirect, url_for
from dotenv import load_dotenv
import mysql.connector
import os
from datetime import datetime, date, timedelta

from app.enums.class_enrollment_status import ClassEnrollmentStatus
from app.enums.session_change_type import SessionChangeType
from app.enums.session_type import SessionType
from app.models.course_profile import CourseProfile
from app.models.scheduled_class_session import ScheduledClassSession
from app.models.student_enrollment_details import StudentEnrollmentDetails
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

from app.dao.student_enrollment_details_dao import StudentEnrollmentDetailsDAO
from app.dao.scheduled_class_session_dao import ScheduledClassSessionDAO
from app.dao.course_profile_dao import CourseProfileDAO
from app.dao.student_profile_dao import StudentProfileDAO
from app.dao.teacher_profile_dao import TeacherProfileDAO
from app.dao.class_schedule_dao import ClassScheduleDAO
from app.dao.classroom_location_dao import ClassroomLocationDAO
from app.dao.semester_dao import SemesterDAO

from app.utils.student_utils import StudentUtils

USERNAME = "dluo"

# Add Enum string names to Enum type conversions here
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

day_of_week_map = {
    "Monday": DayOfWeek.MONDAY,
    "Tuesday": DayOfWeek.TUESDAY,
    "Wednesday": DayOfWeek.WEDNESDAY,
    "Thursday": DayOfWeek.THURSDAY,
    "Friday": DayOfWeek.FRIDAY,
    "Saturday": DayOfWeek.SATURDAY,
    "Sunday": DayOfWeek.SUNDAY
}

# Configure paths
basedir = os.path.abspath(os.path.join(os.path.dirname(__file__)))
template_dir = os.path.join(basedir, 'templates')

# Initialize Flask app
app = Flask(__name__, template_folder=template_dir)
app.secret_key = os.getenv("SECRET_KEY", "dev")

# DB_NAME = os.getenv("DB_NAME", "education_management_test")
#
# def get_connection():
#     try:
#         return mysql.connector.connect(
#             host=os.getenv("DB_HOST"),
#             user=os.getenv("DB_USER"),
#             password=os.getenv("DB_PASSWORD"),
#             database=DB_NAME,
#         )
#     except mysql.connector.Error as err:
#         print(f"Database connection failed: {err}")
#         raise


@app.route('/')
def index():
    return redirect(url_for("home"))

@app.route('/home')
def home():
    return render_template("home_page.html", username=USERNAME)


@app.route('/course-management')
def course_management():
    return render_template("course/course_management.html", username=USERNAME)


@app.route('/student-management')
def student_management():
    return render_template("student/student_management.html", username=USERNAME)


@app.route('/course-management/create-course-profile')
def create_course_profile():
    return render_template("course/create_course_profile_form.html", username=USERNAME)


@app.route('/course-management/course-profile-created', methods=['POST'])
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
    # connection = get_connection()
    # dao = CourseProfileDAO(connection)
    dao = CourseProfileDAO()

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
        return render_template("course/create_course_profile_form.html",
                               form_data=form_data, username=USERNAME)

    if dao.get_course_by_code(course_code):
        flash(f"A course with the code '{course_code}' already exists.", 'warning')
        return render_template("course/create_course_profile_form.html",
                               form_data=form_data, username=USERNAME)


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

    return render_template("course/create_course_profile_success.html",
                           course=course_data, username=USERNAME)


@app.route('/course-management/read_course_profiles')
def read_course_profiles():
    filter_column = request.args.get('filter_column')
    filter_value = request.args.get('filter_value')

    valid_columns = {'course_id', 'course_code', 'course_name', 'profile_status'}
    if filter_column and filter_column not in valid_columns:
        return "Invalid filter column", 400

    try:
        dao = CourseProfileDAO()
        courses = dao.read_course_profiles(filter_column, filter_value)
        for course in courses:
            description = course["course_desc"]
            course["course_desc"] = "" if description is None else description

        return render_template(
            "course/read_course_profiles.html",
            courses=courses,
            filter_column=filter_column,
            filter_value=filter_value,
            username=USERNAME
        )
    except Exception as e:
        return f"Error fetching courses: {e}"

@app.route('/course-management/update-course-profile/search', methods=["GET"])
def update_course_profile_search():
    return render_template("course/update_course_profile_search.html", username=USERNAME)


@app.route('/course-management/update-course-profile/edit-course', methods=['GET'])
def edit_course_profile():
    course_name_or_code = request.args.get('course_name_or_code')

    dao = CourseProfileDAO()
    course_profile = dao.get_course_by_name(course_name_or_code) if dao.get_course_by_name(
        course_name_or_code) else dao.get_course_by_code(course_name_or_code)

    enum_to_string = {
        course_profile.get_target_audience(): AudienceType(course_profile.get_target_audience()).name.title().replace("_", " "),
        course_profile.get_profile_status(): ProfileStatus(course_profile.get_profile_status()).name.title()
    }

    return render_template("course/update_course_profile_edit.html",
                           course=course_profile, enum_to_string=enum_to_string, username=USERNAME)


@app.route('/course-management/update-course-profile/success', methods=['POST'])
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
    dao = CourseProfileDAO()
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

    return render_template("course/update_course_profile_success.html", course=course_data, username=USERNAME)


@app.route('/course-management/delete-course-profile/search', methods=['GET'])
def delete_course_profile_search():
    return render_template("course/delete_course_profile_search.html", username=USERNAME)


@app.route('/course-management/delete-course-profile/success', methods=['POST'])
def delete_course_profile_success():
    course_name_or_code = request.form["course_name_or_code"]

    dao = CourseProfileDAO()
    course_profile = dao.get_course_by_name(course_name_or_code) if dao.get_course_by_name(
        course_name_or_code) else dao.get_course_by_code(course_name_or_code)
    dao.delete_course_profile(course_profile.get_course_id())
    course_data = {
        'course_name': course_profile.get_name(),
        'course_code': course_profile.get_code(),
    }
    return render_template("course/delete_course_profile_success.html", course=course_data, username=USERNAME)


@app.route('/student-management/create-student-profile')
def create_student_profile():
    return render_template("student/create_student_profile_form.html", username=USERNAME)


@app.route('/student-management/student-profile-created', methods=['POST'])
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
    dao = StudentProfileDAO()

    # Check for duplicate email
    if dao.get_student_by_email(email_address):
        flash(f"A student with the email '{email_address}' already exists.", 'warning')
        return render_template("student/create_student_profile_form.html",
                               form_data=form_data, username=USERNAME)

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

    return render_template("student/create_student_profile_success.html",
                           student=student_data, username=USERNAME)


@app.route('/student-management/read_student_profiles')
def read_student_profiles():
    filter_column = request.args.get('filter_column')
    filter_value = request.args.get('filter_value')

    valid_columns = {'student_id', 'first_name', 'last_name', 'profile_status'}

    if filter_column and filter_column not in valid_columns:
        return "Invalid filter column", 400

    try:
        dao = StudentProfileDAO()
        students = dao.read_student_profiles(filter_column, filter_value)

        return render_template(
            "student/read_student_profiles.html",
            students=students,
            filter_column=filter_column,
            filter_value=filter_value,
            username=USERNAME
        )
    except Exception as e:
        return f"Error fetching courses: {e}"


@app.route('/student-management/update-student-profile/search', methods=["GET"])
def update_student_profile_search():
    return render_template("student/update_student_profile_search.html", username=USERNAME)


@app.route('/student-management/update-student-profile/edit-student', methods=['GET'])
def edit_student_profile():
    student_id = request.args.get('student_id')

    if not student_id or not student_id.isdigit():
        flash("Please enter a valid numeric Student ID.", "warning")
        return redirect(url_for('update_student_profile_search'))

    student_id = int(student_id)
    dao = StudentProfileDAO()
    student_profile = dao.get_student_by_id(student_id)

    if student_profile is None:
        flash(f"Student ID {student_id} does not exist.", "warning")
        return redirect(url_for('update_student_profile_search'))

    enum_to_string = {
        student_profile.get_enrollment_status(): EnrollmentStatus(student_profile.get_enrollment_status()).name.title(),
        student_profile.get_guardian_status(): GuardianStatus(student_profile.get_guardian_status()).name.title().replace("_", " "),
        student_profile.get_profile_status(): ProfileStatus(student_profile.get_profile_status()).name.title()
    }

    return render_template("student/update_student_profile_edit.html",
                           student=student_profile, enum_to_string=enum_to_string, username=USERNAME)


@app.route('/student-management/update-student-profile/success', methods=['POST'])
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

    dao = StudentProfileDAO()
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

    return render_template("student/update_student_profile_success.html",
                           student=student_data, username=USERNAME)


@app.route('/class-management/student_enroll')
def student_enrollment_form():

    student_dao = StudentProfileDAO()
    classes_dao = ClassScheduleDAO()

    students = student_dao.read_student_profiles("profile_status", "Active")
    classes = classes_dao.read_class_schedules()
    for c in classes:
        course = classes_dao.get_course_profile_by_schedule_id(c["schedule_id"])
        c["course_name"] = course.get_name()
        c["course_code"] = course.get_code()
    return render_template("student_enrollment_form.html",
                           students=students, classes=classes, username=USERNAME)


@app.route("/class-management/enroll-student-success", methods=["POST"])
def student_enrollment_success():
    student_id = int(request.form["student_id"])
    class_id = int(request.form["class_id"])

    # Check if already enrolled
    student_dao = StudentProfileDAO()
    class_dao = ClassScheduleDAO()
    enrollments_dao = StudentEnrollmentDetailsDAO()

    enrollments = enrollments_dao.read_enrollments("student_id", student_id)

    if any([e["class_schedule_id"] == class_id for e in enrollments]):
        flash("Student is already enrolled in this class.", "warning")
        return redirect(url_for("student_enrollment_form"))
    else:
        student = student_dao.get_student_by_id(student_id)
        class_schedule = class_dao.get_class_schedule_by_id(class_id)
        course = class_dao.get_course_profile_by_schedule_id(class_schedule.get_course_id())
        student_data = {
            "student_id": student.get_student_id(),
            "first_name": student.get_first_name(),
            "last_name": student.get_last_name()
        }
        class_data = {
            "class_id": class_schedule.get_schedule_id(),
            "course_name": course.get_name(),
            "course_code": course.get_code(),
        }

        new_enrollment = StudentEnrollmentDetails(
            0, student_id, class_id, datetime.today(), ClassEnrollmentStatus.ACTIVE
        )
        enrollments_dao.create_enrollment(new_enrollment)

        return render_template("student_enrollment_success.html",
                           student=student_data, class_schedule=class_data, username=USERNAME)


@app.route('/teacher-management')
def teacher_management():
    return render_template("teacher/teacher_management.html", username=USERNAME)


@app.route('/teacher-management/read-teacher-profiles')
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
            "teacher/read_teacher_profiles.html",
            teachers=teachers,
            filter_column=filter_column,
            filter_value=filter_value,
            username=USERNAME
        )
    except Exception as e:
        return f"Error fetching teachers: {e}"


@app.route('/class-management')
def class_management():
    return render_template("class_management.html", username=USERNAME)


@app.route('/class-management/create-class-schedule')
def create_class_schedule():
    connection = get_connection()
    course_profile_dao = CourseProfileDAO(connection)
    active_courses = course_profile_dao.read_course_profiles("profile_status", "Active")
    semester_dao = SemesterDAO(connection)
    semesters = semester_dao.read_semester_data()
    for s in semesters:
        print(s)
    class_types = list(ClassType)
    return render_template("create_class_schedule.html", active_courses=active_courses,
                           semesters=semesters, class_types=class_types, username=USERNAME)


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
        return render_template("create_class_schedule.html",
                               form_data=form_data, username=USERNAME,
                               semesters=..., active_courses=..., classroom_locations=...)

    new_schedule = ClassSchedule(
        schedule_id=0,
        course_id=course_profile.get_course_id(),
        semester_id=semester.get_semester_id(),
        class_capacity=int(class_capacity),
        class_type=class_type,
        class_desc=class_desc
    )

    dao.create_class_schedule(new_schedule)

    return render_template("create_class_schedule_success.html",
                           class_schedule=form_data, username=USERNAME)


@app.route('/class-management/read-class-schedules')
def read_class_schedules():
    filter_column = request.args.get('filter_column')
    filter_value = request.args.get('filter_value')

    valid_columns = {'schedule_id', 'course_id', 'semester_id', 'class_type'}

    if filter_column and filter_column not in valid_columns:
        return "Invalid filter column", 400

    try:
        connection = get_connection()
        dao = ClassScheduleDAO(connection)
        schedules = dao.read_class_schedules(filter_column, filter_value)
        for schedule in schedules:
            course = CourseProfileDAO(connection).get_course_by_id(schedule["course_id"])
            schedule["course_id"] = f"{course.get_code()}: {course.get_name()}"
            semester = SemesterDAO(connection).get_semester_by_id(schedule["semester_id"])
            schedule["semester_id"] = semester.get_name()

        return render_template (
            "class/read_class_schedules.html",
            schedules=schedules,
            filter_column=filter_column,
            filter_value=filter_value,
            username=USERNAME
        )

    except Exception as e:
        return f"Error fetching class schedules: {e}"


@app.route('/class-management/create-scheduled-class-session')
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
                           flags=flags, username=USERNAME)


@app.route('/class-management/scheduled-class-session-created', methods=["POST"])
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
                               username=USERNAME)


@app.route('/class-management/generate-sessions-by-class')
def generate_sessions_by_class():
    course_query = request.args.get('course_query')
    class_sessions = []
    search_attempted = False  # <-- Add this

    if course_query is not None:
        search_attempted = True
        course_query = course_query.strip()
        if course_query.isdigit():
            schedule_id = int(course_query)

            connection = get_connection()
            session_dao = ScheduledClassSessionDAO(connection)

            class_sessions = session_dao.read_class_sessions("schedule_id", schedule_id)
            for session in class_sessions:
                session["location_id"] = (ClassroomLocationDAO(connection)
                                          .get_location_by_id(session["location_id"])).get_name()

            if not class_sessions:
                flash('No sessions found for that schedule ID.', 'warning')
        elif course_query:
            flash('Please enter a valid numeric Schedule ID.', 'warning')

    return render_template('generate_sessions_by_class.html', class_sessions=class_sessions,
                           search_attempted=search_attempted, username=USERNAME)


@app.route('/class-management/generate-schedule-by-student')
def generate_schedule_by_student():
    student_query = request.args.get('student_query')
    schedule_by_date = {}
    search_attempted = False

    if student_query is not None:
        search_attempted = True
        student_query = student_query.strip()

        if student_query.isdigit():
            student_id = int(student_query)

            student_dao = StudentProfileDAO()
            student = student_dao.get_student_by_id(student_id)

            if student:
                enrollment_dao = StudentEnrollmentDetailsDAO()
                enrollments = enrollment_dao.read_enrollments("student_id", student_id)
                session_dao = ScheduledClassSessionDAO()
                location_dao = ClassroomLocationDAO()
                schedule_dao = ClassScheduleDAO()

                for enrollment in enrollments:
                    sessions = session_dao.read_class_sessions('schedule_id', enrollment["class_schedule_id"])
                    for session in sessions:
                        # Replace location ID with actual name
                        session["location_id"] = location_dao.get_location_by_id(session["location_id"]).get_name()
                        # Add course details
                        course_profile = schedule_dao.get_course_profile_by_schedule_id(session["schedule_id"])
                        session["course_code"] = course_profile.get_code()
                        session["course_name"] = course_profile.get_name()
                        # Group by exact date
                        session_date = str(session["scheduled_date"])  # Ensure it's a string for templating
                        if session_date not in schedule_by_date:
                            schedule_by_date[session_date] = []
                        schedule_by_date[session_date].append(session)

                # Sort sessions within each date
                for date_sessions in schedule_by_date.values():
                    date_sessions.sort(key=lambda x: x["seq_no"])
            else:
                flash('No student found with that ID.', 'warning')
        elif student_query:
            flash('Please enter a valid numeric Student ID.', 'warning')

    return render_template('generate_schedule_by_student.html',
                           schedule_by_date=schedule_by_date,
                           search_attempted=search_attempted,
                           username=USERNAME)


if __name__ == '__main__':
    app.run(debug=True)
