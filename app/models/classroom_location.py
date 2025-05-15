class ClassroomLocation(object):
    def __init__(self, location_id, room_number, building_name, capacity):
        self.__location_id = location_id
        self.__room_number = room_number
        self.__building_name = building_name
        self.__capacity = capacity

    def get_name(self):
        return f"{self.__building_name} {self.__room_number}"

    def get_location_id(self):
        return self.__location_id

    def get_room_number(self):
        return self.__room_number

    def get_building_name(self):
        return self.__building_name

    def get_capacity(self):
        return self.__capacity
