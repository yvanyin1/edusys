from app.enums.enrollment_status import EnrollmentStatus
from app.enums.guardian_status import GuardianStatus
from app.enums.profile_status import ProfileStatus


class StudentProfile(object):

    def __init__(self, student_id, first_name, middle_name, last_name, birth_date, phone_number, email_address,
                 home_address, registration_date, enrollment_status, guardian_status, profile_status):
        self.__student_id = student_id
        self.__first_name = first_name
        self.__middle_name = middle_name
        self.__last_name = last_name
        self.__birth_date = birth_date
        self.__phone_number = phone_number
        self.__email_address = email_address
        self.__home_address = home_address
        self.__registration_date = registration_date
        if isinstance(enrollment_status, EnrollmentStatus):
            self.__enrollment_status = enrollment_status
        else:
            raise Exception('enrollment_status must be of type EnrollmentStatus')
        if isinstance(guardian_status, GuardianStatus):
            self.__guardian_status = guardian_status
        else:
            raise Exception('guardian_status must be of type GuardianStatus')
        if isinstance(profile_status, ProfileStatus):
            self.__profile_status = profile_status
        else:
            raise Exception("profile_status must be of type ProfileStatus")

    def __eq__(self, other):
        if not isinstance(other, StudentProfile):
            return False
        return self.__student_id == other.__student_id

    def __hash__(self):
        return hash((self.__student_id, self.__first_name, self.__middle_name, self.__last_name, self.__birth_date))

    def __repr__(self):
        return (f"StudentProfile({self.__student_id}), {self.__first_name}, {self.__middle_name}, " +
                f"{self.__last_name}, {self.__birth_date}), {self.__phone_number}, {self.__email_address}, " +
                f"{self.__home_address}, {self.__registration_date}, {self.__enrollment_status}, " +
                f"{self.__guardian_status}, {self.__profile_status})")

    def __str__(self):
        return f"{self.__student_id}: {self.__first_name} {self.__middle_name} {self.__last_name}"

    def get_student_id(self):
        return self.__student_id

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

    def get_registration_date(self):
        return self.__registration_date

    def set_registration_date(self, registration_date):
        self.__registration_date = registration_date

    def get_enrollment_status(self):
        return self.__enrollment_status

    def set_enrollment_status(self, enrollment_status):
        self.__enrollment_status = enrollment_status

    def get_guardian_status(self):
        return self.__guardian_status

    def set_guardian_status(self, guardian_status):
        self.__guardian_status = guardian_status

    def get_profile_status(self):
        return self.__profile_status

    def set_profile_status(self, profile_status):
        self.__profile_status = profile_status
