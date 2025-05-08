from app.dao.base_dao import BaseDAO
from app.enums.day_of_week import DayOfWeek
from app.enums.session_type import SessionType
from app.enums.session_change_type import SessionChangeType
from app.enums.flag import Flag
from app.models.course_profile import CourseProfile
from app.models.scheduled_class_session import ScheduledClassSession


class ScheduledClassSessionDAO(BaseDAO):

    def __init__(self, connection):
        super().__init__(connection, "scheduled_class_session")

    def get_class_session_by_id(self, session_id: int) -> ScheduledClassSession | None:
        result = self.get_rows_by_column_value(session_id, "scheduled_class_session")
        if result:
            return self.build_entity_object(result[0])
        return None

    def create_class_session(self, session: ScheduledClassSession):
        query = """
                INSERT INTO scheduled_class_session
                (schedule_id, location_id, day_of_week, start_time, end_time, session_type, scheduled_date, seq_no, session_change_type, flag)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) \
                """
        values = (
            session.get_schedule_id(),
            session.get_location_id(),
            session.get_day_of_week().value,
            session.get_start_time(),
            session.get_end_time(),
            session.get_session_type().value,
            session.get_scheduled_date(),
            session.get_seq_no(),
            session.get_session_change_type().value if session.get_session_change_type() else None,
            session.get_flag().value
        )
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, values)
        conn.commit()
        return cursor.lastrowid

    def read_class_sessions(self, filter_column=None, filter_value=None):
        try:
            query = "SELECT * FROM scheduled_class_session"
            if filter_column and filter_value:
                query += f" WHERE {filter_column} LIKE '%{filter_value}%'"
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)  # Enable fetching data as a dictionary
            cursor.execute(query)
            sessions = cursor.fetchall()

            # Convert Enum integer values to Enum name
            for session in sessions:
                session["day_of_week"] = DayOfWeek(session["day_of_week"]).name.title()
                session["session_type"] = SessionType(session["session_type"]).name.title()

                session_change_type_val = session.get("session_change_type")
                session["session_change_type"] = (
                    SessionChangeType(session_change_type_val).name.title().replace("_", " ")
                    if session_change_type_val is not None else None
                )
                session["flag"] = Flag(session["flag"]).name.title()

            return sessions

        except Exception as e:
            return f"Error fetching class schedules: {e}"

    @staticmethod
    def build_entity_object(row: dict) -> ScheduledClassSession:
        return ScheduledClassSession(
            session_id=row["session_id"],
            schedule_id=row["schedule_id"],
            location_id=row["location_id"],
            day_of_week=DayOfWeek(row["day_of_week"]),
            start_time=row["start_time"],
            end_time=row["end_time"],
            session_type=SessionType(row["session_type"]),
            scheduled_date=row["scheduled_date"],
            seq_no=row["seq_no"],
            session_change_type=SessionChangeType(row["session_change_type"]),
            flag=Flag(row["flag"])
        )