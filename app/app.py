from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import mysql.connector
import os

load_dotenv(dotenv_path='.env_test')

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
template_dir = os.path.join(basedir, 'templates')

app = Flask(__name__, template_folder=template_dir)

print("Template folder being used:", app.template_folder)

# Configure SQLAlchemy with MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/education_management_test"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

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

        # SQL query to insert initial data
        cursor.execute("DROP TABLE IF EXISTS course_profile")
        cursor.execute("""CREATE TABLE course_profile (
            course_id INT NOT NULL AUTO_INCREMENT,  -- for some reason adding NOT NULL removes an error
            course_name VARCHAR(50) NOT NULL UNIQUE,
            course_code VARCHAR(10) NOT NULL UNIQUE,
            course_desc TEXT,
            target_audience TINYINT DEFAULT 1 CHECK (target_audience IN (1, 2)),
            duration_in_weeks TINYINT,
            credit_hours FLOAT,
            profile_status TINYINT NOT NULL DEFAULT 0 CHECK (profile_status IN (0, 1)),
            PRIMARY KEY (course_id)
        );""")
        sql_insert = """
            INSERT INTO course_profile(course_name, course_code, course_desc, target_audience, duration_in_weeks, credit_hours, profile_status)
            VALUES ('Introduction to Computer Science', 'COMP 250', 'Searching/sorting algorithms, data structures', 2, 15, 3.0, 1),
                   ('Theory of Computation', 'COMP 330', NULL, 2, 12, 3.0, 1),
                   ('Sampling Theory and Applications', 'MATH 525', 'Horvitz-Thompson estimator', 1, 10, 3.0, 1);
        """

        # Execute the SQL insert query
        cursor.execute(sql_insert)
        connection.commit()
        cursor.close()
        connection.close()

    except Exception as e:
        print(f"Error loading initial data: {e}")

# TODO for testing purposes
load_initial_data()


@app.route('/')
def home():
    return "Hello, World!"


@app.route('/course-management')
def course_management():
    return render_template("index.html", username="dluo")


@app.route('/create-course-profile')
def create_course_profile():
    return render_template("create_course_profile_form.html", username="dluo")


@app.route('/course-created', methods=['POST'])
def course_profile_created():
    course_data = {
        'course_name': request.form['course_name'],
        'course_code': request.form['course_code'],
        'course_desc': request.form['course_desc'],
        'target_audience': request.form['target_audience'],
        'duration_in_weeks': request.form['duration_in_weeks'],
        'prerequisites': request.form['prerequisites'],
        'corequisites': request.form['corequisites'],
        'credit_hours': request.form['credit_hours']
    }
    return render_template("create_course_profile_success.html", course=course_data)


@app.route('/view-course-profiles')
def view_courses():
    try:
        # Query all courses from the 'course_profile' table
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
        )
        cursor = connection.cursor(dictionary=True)  # Enable fetching data as a dictionary
        cursor.execute("SELECT * FROM course_profile")
        courses = cursor.fetchall()  # Get all rows as a list of dictionaries

        cursor.close()
        connection.close()

        # Pass the courses data to the template
        return render_template("view_course-profiles.html", courses=courses)
    except Exception as e:
        return f"Error fetching courses: {e}"


if __name__ == '__main__':
    app.run(debug=True)