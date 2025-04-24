import mysql.connector
from app.models.course_profile import CourseProfile
from app.enums.audience_type import AudienceType
from app.enums.profile_status import ProfileStatus

class CourseProfileDAO:

    def __init__(self, connection):
        self.__connection = connection

    def get_connection(self):
        return self.__connection

    def count_course_profiles(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM course_profile')
        return cursor.fetchone()[0]

    def get_max_course_id(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(course_id) FROM course_profile")
        return cursor.fetchone()[0]

    def get_rows(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM course_profile")
        return cursor.fetchall()

    def create_course_profile(self, course_profile: CourseProfile):
        # course
        query = """
        INSERT INTO course_profile 
        (course_name, course_code, course_desc, target_audience, duration_in_weeks, credit_hours, profile_status)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            course_profile.get_name(),
            course_profile.get_code(),
            course_profile.get_description(),
            course_profile.get_target_audience().value,
            course_profile.get_duration_in_weeks(),
            course_profile.get_credit_hours(),
            course_profile.get_profile_status().value
        )
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, values)
        conn.commit()
        return cursor.lastrowid

    def get_course_by_id(self, course_id: int) -> CourseProfile | None:
        query = "SELECT * FROM course_profile WHERE course_id = %s"
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, (course_id,))
        result = cursor.fetchone()
        if result:
            return self.build_course_object(result)
        return None

    def update_course(self, course_profile: CourseProfile):
        query = """
        UPDATE course_profile SET
            course_name = %s,
            course_code = %s,
            course_desc = %s,
            target_audience = %s,
            duration_in_weeks = %s,
            credit_hours = %s,
            profile_status = %s
        WHERE course_id = %s
        """
        values = (
            course_profile.get_name(),
            course_profile.get_code(),
            course_profile.get_description(),
            course_profile.get_target_audience().value,
            course_profile.get_duration_in_weeks(),
            course_profile.get_credit_hours(),
            course_profile.get_profile_status().value,
            course_profile.get_course_id()
        )
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, values)
        conn.commit()

    def delete_course(self, course_id: int):
        query = "DELETE FROM course_profile WHERE course_id = %s"
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (course_id,))
        conn.commit()

    @staticmethod
    def build_course_object(row):
        return CourseProfile(
            course_id=row['course_id'],
            course_name=row['course_name'],
            course_code=row['course_code'],
            course_desc=row['course_desc'],
            target_audience=AudienceType(row['target_audience']),
            duration_in_weeks=row['duration_in_weeks'],
            credit_hours=row['credit_hours'],
            profile_status=ProfileStatus(row['profile_status']),
        )