from abc import ABC, abstractmethod
from course_request import CourseRequest
from datetime import datetime

class User(ABC):

    def __init__(self, first_name, last_name, username, email, password_hash):
        self._first_name = first_name
        self._last_name = last_name
        self._username = username
        self._email = email
        self._password_hash = password_hash

    @property
    def get_first_name(self):
        return self._first_name

    def get_last_name(self):
        return self._last_name

    def get_username(self):
        return self._username

    def get_email(self):
        return self._email

    def get_password_hash(self):
        return self._password_hash


class AcademicStaff(User):

    def request_course(self, course, catalog):
        if course.get_code() in [c.get_code() for c in catalog.get_courses()]:
            raise Exception("Course code already exists in catalog")
        # have another conditional for course code format

        return CourseRequest(123, self, course, datetime.now())


class Administrator(User):

    def set_course_request_status(self, request, request_status):
        pass

    def register_course(self, course, catalog):
        catalog.add_course(course)
