from app.dao.base_dao import BaseDAO
from app.models.course_profile import CourseProfile
from app.enums.audience_type import AudienceType
from app.enums.profile_status import ProfileStatus


class CourseProfileDAO(BaseDAO):

    def __init__(self, connection=None):
        super().__init__("course_profile", connection)

    def get_course_by_id(self, course_id: int) -> CourseProfile | None:
        try:
            result = self.get_rows_by_column_value(course_id, "course_id")
            if result:
                return self.build_entity_object(result[0])
            return None
        except Exception as e:
            print(f"Error fetching course by ID: {e}")
            return None

    def get_course_by_name(self, course_name: str) -> CourseProfile | None:
        try:
            result = self.get_rows_by_column_value(course_name, "course_name")
            if result:
                return self.build_entity_object(result[0])
            return None
        except Exception as e:
            print(f"Error fetching course by name: {e}")
            return None

    def get_course_by_code(self, course_code: str) -> CourseProfile | None:
        try:
            result = self.get_rows_by_column_value(course_code, "course_code")
            if result:
                return self.build_entity_object(result[0])
            return None
        except Exception as e:
            print(f"Error fetching course by code: {e}")
            return None

    def create_course_profile(self, course_profile: CourseProfile):
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

        conn = None
        cursor = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, values)
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error creating course profile: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def read_course_profiles(self, filter_column=None, filter_value=None):
        conn = None
        cursor = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM course_profile")
            courses = cursor.fetchall()

            for course in courses:
                course["target_audience"] = AudienceType(course["target_audience"]).name.title().replace("_", " ")
                course["profile_status"] = ProfileStatus(course["profile_status"]).name.title()

            if filter_column and filter_value:
                filter_value_lower = filter_value.lower()
                courses = [
                    course for course in courses
                    if filter_column in course and filter_value_lower in str(course[filter_column]).lower()
                ]

            return courses
        except Exception as e:
            return f"Error fetching courses: {e}"
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def update_course_profile(self, course_profile: CourseProfile):
        query = """
            UPDATE course_profile
            SET course_name = %s,
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

        conn = None
        cursor = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, values)
            conn.commit()
            if cursor.rowcount == 0:
                raise ValueError(f"Course ID {course_profile.get_course_id()} does not exist in the database.")
        except Exception as e:
            print(f"Error updating course profile: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def delete_course_profile(self, course_id: int):
        query = "DELETE FROM course_profile WHERE course_id = %s"
        conn = None
        cursor = None

        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, (course_id,))
            conn.commit()
            if cursor.rowcount == 0:
                raise ValueError(f"Course ID {course_id} does not exist in the database.")
        except Exception as e:
            print(f"Error deleting course profile: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @staticmethod
    def build_entity_object(row: dict) -> CourseProfile:
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