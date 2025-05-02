from app.enums.class_enrollment_status import ClassEnrollmentStatus

class StudentEnrollmentDetails(object):

    def __init__(self, enrollment_id, student_id, class_schedule_id, enrollment_date, enrollment_status):
        self.__enrollment_id = enrollment_id
        self.__student_id = student_id
        self.__class_schedule_id = class_schedule_id
        self.__enrollment_date = enrollment_date
        if isinstance(enrollment_status, ClassEnrollmentStatus):
            self.__enrollment_status = enrollment_status
        else:
            raise Exception("enrollment_status must be of type ClassEnrollmentStatus")

    def get_enrollment_id(self):
        return self.__enrollment_id

    def get_student_id(self):
        return self.__student_id

    def get_class_schedule_id(self):
        return self.__class_schedule_id

    def get_enrollment_date(self):
        return self.__enrollment_date

    def set_enrollment_date(self, enrollment_date):
        self.__enrollment_date = enrollment_date

    def get_enrollment_status(self):
        return self.__enrollment_status

    def set_enrollment_status(self, enrollment_status):
        self.__enrollment_status = enrollment_status
