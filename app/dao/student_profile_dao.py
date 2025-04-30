from app.dao.base_dao import BaseDAO
from app.models.student_profile import StudentProfile
from app.enums.enrollment_status import EnrollmentStatus
from app.enums.guardian_status import GuardianStatus
from app.enums.profile_status import ProfileStatus

class StudentProfileDAO(BaseDAO):

    def __init__(self, connection):
        super().__init__(connection, "student_profile")

    def get_student_by_id(self, student_id: int) -> StudentProfile | None:
        result = self.get_rows_by_column_value(student_id, "student_id")
        if result:
            return self.build_entity_object(result[0])
        return None

    def get_student_by_email(self, email: str) -> StudentProfile | None:
        result = self.get_rows_by_column_value(email, "email_address")
        if result:
            return self.build_entity_object(result[0])
        return None

    def create_student_profile(self, student_profile: StudentProfile):
        query = """
        INSERT INTO student_profile 
        (first_name, middle_name, last_name, birth_date, phone_number, email_address, home_address, registration_date, enrollment_status, guardian_status, profile_status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            student_profile.get_first_name(),
            student_profile.get_middle_name(),
            student_profile.get_last_name(),
            student_profile.get_birth_date(),
            student_profile.get_phone_number(),
            student_profile.get_email_address(),
            student_profile.get_home_address(),
            student_profile.get_registration_date(),
            student_profile.get_enrollment_status().value,
            student_profile.get_guardian_status().value,
            student_profile.get_profile_status().value
        )
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, values)
        conn.commit()
        return cursor.lastrowid

    @staticmethod
    def build_entity_object(row: dict) -> StudentProfile:
        return StudentProfile(
            student_id=row['student_id'],
            first_name=row['first_name'],
            middle_name=row['middle_name'],
            last_name=row['last_name'],
            birth_date=row['birth_date'],
            phone_number=row['phone_number'],
            email_address=row['email_address'],
            home_address=row['home_address'],
            registration_date=row['registration_date'],
            enrollment_status=row['enrollment_status'],
            guardian_status=row['guardian_status'],
            profile_status=row['profile_status'])