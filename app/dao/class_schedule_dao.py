from app.dao.base_dao import BaseDAO
from app.models.class_schedule import ClassSchedule
from app.enums.class_type import ClassType
from app.dao.course_profile_dao import CourseProfileDAO


class ClassScheduleDAO(BaseDAO):

    def __init__(self, connection=None):
        super().__init__("class_schedule", connection)

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
        conn = None
        cursor = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, values)
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error creating class schedule: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def read_class_schedules(self, filter_column=None, filter_value=None):
        conn = None
        cursor = None
        try:
            query = "SELECT * FROM class_schedule"
            if filter_column and filter_value:
                query += f" WHERE {filter_column} LIKE '%{filter_value}%'"
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query)
            class_schedules = cursor.fetchall()

            for class_schedule in class_schedules:
                class_schedule["class_type"] = ClassType(class_schedule["class_type"]).name.title().replace("_", "-")
            return class_schedules

        except Exception as e:
            return f"Error fetching class schedules: {e}"

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_course_profile_by_schedule_id(self, schedule_id):
        conn = None
        try:
            class_schedule = self.get_class_schedule_by_id(schedule_id)
            conn = self.get_connection()
            return CourseProfileDAO(conn).get_course_by_id(class_schedule.get_course_id())
        except Exception as e:
            print(f"Error fetching course profile for schedule ID {schedule_id}: {e}")
            raise
        finally:
            if conn:
                conn.close()

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