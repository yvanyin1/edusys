from flask import Flask, render_template
import os

app = Flask(__name__, template_folder=os.path.join(os.getcwd(), 'templates'))


@app.route('/')
def home():
    return "Hello, World!"

@app.route('/course-management')
def course_management():
    return render_template("index.html", username="dluo")


if __name__ == '__main__':
    app.run(debug=True)