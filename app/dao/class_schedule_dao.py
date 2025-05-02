from app.dao.base_dao import BaseDAO
from app.models.class_schedule import ClassSchedule
from app.enums.class_type import ClassType
from app.enums.audience_type import AudienceType
from app.enums.profile_status import ProfileStatus

from app.dao.course_profile_dao import CourseProfileDAO
from app.models.course_profile import CourseProfile


class ClassScheduleDAO(BaseDAO):

    def __init__(self, connection):
        super().__init__(connection, "class_schedule")

    def get_class_schedule_by_id(self, schedule_id: int) -> ClassSchedule | None:
        result = self.get_rows_by_column_value(schedule_id, "schedule_id")
        if result:
            return self.build_entity_object(result[0])
        return None

    def create_class_schedule(self, class_schedule: ClassSchedule):
        query = """
        INSERT INTO class_schedule 
        (course_id, semester_id, class_capacity, class_type, class_desc)
        VALUES (%s, %s, %s, %s, %s)
        """
        values = (
            class_schedule.get_course_id(),
            class_schedule.get_semester_id(),
            class_schedule.get_class_capacity(),
            class_schedule.get_class_type().value,
            class_schedule.get_class_desc(),
        )
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, values)
        conn.commit()
        return cursor.lastrowid

    def read_class_schedules(self, filter_column=None, filter_value=None):
        try:
            query = "SELECT * FROM class_schedule"
            if filter_column and filter_value:
                query += f" WHERE {filter_column} LIKE '%{filter_value}%'"
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)  # Enable fetching data as a dictionary
            cursor.execute(query)
            class_schedules = cursor.fetchall()
            conn.commit()

            # Convert Enum integer values to Enum name
            for class_schedule in class_schedules:
                class_schedule["class_type"] = ClassType(class_schedule["class_type"]).name.title().replace("_", "-")
            return class_schedules

        except Exception as e:
            return f"Error fetching class schedules: {e}"

    def get_course_profile_by_schedule_id(self, schedule_id):
        class_schedule = self.get_class_schedule_by_id(schedule_id)
        course_id = class_schedule.get_course_id()
        return CourseProfileDAO(self.get_connection()).get_course_by_id(course_id)

    @staticmethod
    def build_entity_object(row: dict) -> ClassSchedule:
        return ClassSchedule(
            schedule_id=row["schedule_id"],
            course_id=row["course_id"],
            semester_id=row["semester_id"],
            class_capacity=row["class_capacity"],
            class_type=ClassType(row["class_type"]),
            class_desc=row["class_desc"],
        )