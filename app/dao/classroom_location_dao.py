from app.dao.base_dao import BaseDAO
from app.models.classroom_location import ClassroomLocation

class ClassroomLocationDAO(BaseDAO):

    def __init__(self, connection=None):
        super().__init__("classroom_location", connection)

    def get_location_by_id(self, location_id: int) -> ClassroomLocation | None:
        result = self.get_rows_by_column_value(location_id, "location_id")
        if result:
            return self.build_entity_object(result[0])
        return None

    def read_classroom_location_data(self, filter_column=None, filter_value=None):
        try:
            query = "SELECT * FROM classroom_location"
            if filter_column and filter_value:
                query += f" WHERE {filter_column} LIKE '%{filter_value}%'"
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)  # Enable fetching data as a dictionary
            cursor.execute(query)
            classroom_locations = cursor.fetchall()
            return classroom_locations

        except Exception as e:
            return f"Error fetching semesters: {e}"

    @staticmethod
    def build_entity_object(row: dict) -> ClassroomLocation:
        return ClassroomLocation (
            location_id=row["location_id"],
            room_number=row["room_number"],
            building_name=row["building_name"],
            capacity=row["capacity"],
        )