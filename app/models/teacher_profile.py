from app.enums.employment_status import EmploymentStatus
from app.enums.teacher_role import TeacherRole
from app.enums.profile_status import ProfileStatus


class TeacherProfile(object):

    def __init__(self, teacher_id, first_name, middle_name, last_name, birth_date, phone_number, email_address,
                 home_address, subject_expertise, employment_status, teacher_role, profile_status):
        self.__teacher_id = teacher_id
        self.__first_name = first_name
        self.__middle_name = middle_name
        self.__last_name = last_name
        self.__birth_date = birth_date
        self.__phone_number = phone_number
        self.__email_address = email_address
        self.__home_address = home_address
        self.__subject_expertise = subject_expertise
        if isinstance(employment_status, EmploymentStatus):
            self.__employment_status = employment_status
        else:
            raise Exception('employment_status must be of type EmploymentStatus')
        if isinstance(teacher_role, TeacherRole):
            self.__teacher_role = teacher_role
        else:
            raise Exception('teacher_role must be of type TeacherRole')
        if isinstance(profile_status, ProfileStatus):
            self.__profile_status = profile_status
        else:
            raise Exception("profile_status must be of type ProfileStatus")

    def __eq__(self, other):
        if not isinstance(other, TeacherProfile):
            return False
        return self.__teacher_id == other.__teacher_id

    def __hash__(self):
        return hash((self.__teacher_id, self.__first_name, self.__middle_name, self.__last_name, self.__birth_date))

    def __repr__(self):
        return (f"TeacherProfile({self.__teacher_id}), {self.__first_name}, {self.__middle_name}, " +
                f"{self.__last_name}, {self.__birth_date}), {self.__phone_number}, {self.__email_address}, " +
                f"{self.__home_address}, {self.__subject_expertise}, {self.__employment_status}, " +
                f"{self.__teacher_role}, {self.__profile_status})")

    def __str__(self):
        return f"{self.__teacher_id}: {self.__first_name} {self.__middle_name} {self.__last_name}"

    def get_student_id(self):
        return self.__teacher_id

    def get_first_name(self):
        return self.__first_name

    def set_first_name(self, first_name):
        self.__first_name = first_name

    def get_middle_name(self):
        return self.__middle_name

    def set_middle_name(self, middle_name):
        self.__middle_name = middle_name

    def get_last_name(self):
        return self.__last_name

    def set_last_name(self, last_name):
        self.__last_name = last_name

    def get_full_name_self(self):
        return self.__first_name + " " + self.__middle_name + " " + self.__last_name

    def get_birth_date(self):
        return self.__birth_date

    def set_birth_date(self, birth_date):
        self.__birth_date = birth_date

    def get_phone_number(self):
        return self.__phone_number

    def set_phone_number(self, phone_number):
        return self.__phone_number

    def get_email_address(self):
        return self.__email_address

    def set_email_address(self, email_address):
        self.__email_address = email_address

    def get_home_address(self):
        return self.__home_address

    def set_home_address(self, home_address):
        self.__home_address = home_address

    def get_subject_expertise(self):
        return self.__subject_expertise

    def set_subject_expertise(self, subject_expertise):
        self.__subject_expertise = subject_expertise

    def get_employment_status(self):
        return self.__employment_status

    def set_employment_status(self, employment_status):
        if isinstance(employment_status, EmploymentStatus):
            self.__employment_status = employment_status
        else:
            raise Exception('employment_status must be of type EmploymentStatus')

    def get_teacher_role(self):
        return self.__teacher_role

    def set_teacher_role(self, teacher_role):
        if isinstance(teacher_role, TeacherRole):
            self.__teacher_role = teacher_role
        else:
            raise Exception('teacher_role must be of type TeacherRole')

    def get_profile_status(self):
        return self.__profile_status

    def set_profile_status(self, profile_status):
        if isinstance(profile_status, ProfileStatus):
            self.__profile_status = profile_status
        else:
            raise Exception("profile_status must be of type ProfileStatus")
