from app.dao.base_dao import BaseDAO
from app.models.teacher_profile import TeacherProfile
from app.enums.employment_status import EmploymentStatus
from app.enums.teacher_role import TeacherRole
from app.enums.profile_status import ProfileStatus

class TeacherProfileDAO(BaseDAO):

    def __init__(self, connection):
        super().__init__(connection, "teacher_profile")

    def get_teacher_by_id(self, teacher_id: int) -> TeacherProfile | None:
        result = self.get_rows_by_column_value(teacher_id, "teacher_id")
        if result:
            return self.build_entity_object(result[0])
        return None

    def get_teacher_by_email(self, email: str) -> TeacherProfile | None:
        result = self.get_rows_by_column_value(email, "email_address")
        if result:
            return self.build_entity_object(result[0])
        return None

    def get_max_teacher_id(self):
        return self.get_max_element_in_column("teacher_id")

    def create_teacher_profile(self, teacher_profile: TeacherProfile):
        query = """
        INSERT INTO teacher_profile 
        (first_name, middle_name, last_name, birth_date,
        phone_number, email_address, home_address, subject_expertise,
         employment_status, teacher_role, profile_status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            teacher_profile.get_first_name(),
            teacher_profile.get_middle_name(),
            teacher_profile.get_last_name(),
            teacher_profile.get_birth_date(),
            teacher_profile.get_phone_number(),
            teacher_profile.get_email_address(),
            teacher_profile.get_home_address(),
            teacher_profile.get_subject_expertise(),
            teacher_profile.get_employment_status().value,
            teacher_profile.get_teacher_role().value,
            teacher_profile.get_profile_status().value
        )
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, values)
        conn.commit()
        return cursor.lastrowid

    def read_teacher_profiles(self, filter_column=None, filter_value=None):
        try:
            query = "SELECT * FROM teacher_profile"
            if filter_column and filter_value:
                query += f" WHERE {filter_column} LIKE '%{filter_value}%'"
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)  # Enable fetching data as a dictionary
            cursor.execute(query)
            teachers = cursor.fetchall()

            # Convert Enum integer values to Enum name
            for teacher in teachers:
                teacher["employment_status"] = EmploymentStatus(teacher["employment_status"]).name.title().replace("_", "-")
                enum_role = TeacherRole(teacher["teacher_role"])
                teacher["teacher_role"] = "TA" if enum_role == TeacherRole.TA else TeacherRole(teacher["teacher_role"]).name.title()
                teacher["profile_status"] = ProfileStatus(teacher["profile_status"]).name.title()
            return teachers

        except Exception as e:
            return f"Error fetching teachers: {e}"

    @staticmethod
    def build_entity_object(row: dict) -> TeacherProfile:
        return TeacherProfile(
            teacher_id=row['teacher_id'],
            first_name=row['first_name'],
            middle_name=row['middle_name'],
            last_name=row['last_name'],
            birth_date=row['birth_date'],
            phone_number=row['phone_number'],
            email_address=row['email_address'],
            home_address=row['home_address'],
            subject_expertise=row['subject_expertise'],
            employment_status=EmploymentStatus(row['employment_status']),
            teacher_role=TeacherRole(row['teacher_role']),
            profile_status=ProfileStatus(row['profile_status']))
