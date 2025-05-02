from app.dao.base_dao import BaseDAO
from app.models.student_enrollment_details import StudentEnrollmentDetails
from app.enums.class_enrollment_status import ClassEnrollmentStatus


class StudentEnrollmentDetailsDAO(BaseDAO):

    def __init__(self, connection):
        super().__init__(connection, "student_enrollment_details")

    def get_enrollment_by_id(self, enrollment_id: int) -> StudentEnrollmentDetails | None:
        result = self.get_rows_by_column_value(enrollment_id, "enrollment_id")
        if result:
            return self.build_entity_object(result[0])
        return None

    def create_enrollment(self, enrollment: StudentEnrollmentDetails):
        query = """
        INSERT INTO student_enrollment_details
        (student_id, class_schedule_id, enrollment_date, enrollment_status)
        VALUES (%s, %s, %s, %s)
        """
        values = (
            enrollment.get_student_id(),
            enrollment.get_class_schedule_id(),
            enrollment.get_enrollment_date(),
            enrollment.get_enrollment_status().value,
        )
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, values)
        conn.commit()
        return cursor.lastrowid

    def read_enrollments(self, filter_column=None, filter_value=None):
        try:
            query = "SELECT * FROM student_enrollment_details"
            if filter_column and filter_value:
                query += f" WHERE {filter_column} LIKE '%{filter_value}%'"
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query)
            enrollments = cursor.fetchall()
            conn.commit()

            for enrollment in enrollments:
                enrollment["enrollment_status"] = ClassEnrollmentStatus(enrollment["enrollment_status"]).name.title()
            return enrollments

        except Exception as e:
            return f"Error fetching enrollment records: {e}"

    @staticmethod
    def build_entity_object(row: dict) -> StudentEnrollmentDetails:
        print(row["enrollment_date"])
        return StudentEnrollmentDetails(
            enrollment_id=row["enrollment_id"],
            student_id=row["student_id"],
            class_schedule_id=row["class_schedule_id"],
            enrollment_date=row["enrollment_date"],
            enrollment_status=ClassEnrollmentStatus(row["enrollment_status"]),
        )