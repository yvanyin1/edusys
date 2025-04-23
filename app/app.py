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


if __name__ == '__main__':
    app.run(debug=True)