from app.dao.base_dao import BaseDAO
from app.enums.season import Season
from app.models.semester import Semester

class SemesterDAO(BaseDAO):

    def __init__(self, connection):
        super().__init__(connection, "semester")

    def get_semester_by_id(self, semester_id: int) -> Semester | None:
        result = self.get_rows_by_column_value(semester_id, "semester_id")
        if result:
            return self.build_entity_object(result[0])
        return None

    def read_semester_data(self, filter_column=None, filter_value=None):
        try:
            query = "SELECT * FROM semester"
            if filter_column and filter_value:
                query += f" WHERE {filter_column} LIKE '%{filter_value}%'"
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)  # Enable fetching data as a dictionary
            cursor.execute(query)
            semesters = cursor.fetchall()
            conn.commit()

            # Convert Enum integer values to Enum name
            for semester in semesters:
                semester["season"] = Season(semester["season"]).name.title()
            return semesters

        except Exception as e:
            return f"Error fetching semesters: {e}"

    @staticmethod
    def build_entity_object(row: dict) -> Semester:
        return Semester(
            semester_id=row["semester_id"],
            season=Season(row["season"]),
            academic_year=row["academic_year"],
            start_date=row["start_date"],
            end_date=row["end_date"],
            registration_deadline=row["registration_deadline"],
            withdrawal_deadline=row["withdrawal_deadline"],
        )