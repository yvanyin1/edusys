from app.dao.base_dao import BaseDAO
from app.enums.day_of_week import DayOfWeek
from app.enums.session_type import SessionType
from app.enums.session_change_type import SessionChangeType
from app.enums.flag import Flag
from app.models.course_profile import CourseProfile
from app.models.scheduled_class_session import ScheduledClassSession


class ScheduledClassSessionDAO(BaseDAO):

    def __init__(self, connection=None):
        super().__init__("scheduled_class_session", connection)

    def get_class_session_by_id(self, session_id: int) -> ScheduledClassSession | None:
        result = self.get_rows_by_column_value(session_id, "session_id")
        if result:
            return self.build_entity_object(result[0])
        return None

    def create_class_session(self, session: ScheduledClassSession):
        query = """
                INSERT INTO scheduled_class_session
                (schedule_id, location_id, day_of_week, start_time, end_time, session_type,
                 scheduled_date, seq_no, session_change_type, flag)
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

        conn = None
        cursor = None
        try:
            conn = self.get_connection()
            print("Connection status:", conn.is_connected())
            cursor = conn.cursor()
            cursor.execute(query, values)
            conn.commit()
            return cursor.lastrowid

        except Exception as e:
            conn.rollback()
            raise RuntimeError(f"Failed to create class session: {e}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def read_class_sessions(self, filter_column=None, filter_value=None):
        cursor = None
        conn = None
        try:
            query = "SELECT * FROM scheduled_class_session"
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query)
            sessions = cursor.fetchall()

            # Convert enum integers to readable names
            for session in sessions:
                session["day_of_week"] = DayOfWeek(session["day_of_week"]).name.title()
                session["session_type"] = SessionType(session["session_type"]).name.title()
                session_change_type_val = session.get("session_change_type")
                session["session_change_type"] = (
                    SessionChangeType(session_change_type_val).name.title().replace("_", " ")
                    if session_change_type_val is not None else None
                )
                session["flag"] = Flag(session["flag"]).name.title()

            # Filter in Python safely
            if filter_column and filter_value:
                filter_value_lower = filter_value.lower()
                sessions = [
                    session for session in sessions
                    if filter_column in session and filter_value_lower in str(session[filter_column]).lower()
                ]

            return sessions

        except Exception as e:
            return f"Error fetching class schedules: {e}"

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

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
