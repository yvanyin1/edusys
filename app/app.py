from flask import Flask, render_template, request
import os

app = Flask(__name__, template_folder=os.path.join(os.getcwd(), 'templates'))


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


if __name__ == '__main__':
    app.run(debug=True)