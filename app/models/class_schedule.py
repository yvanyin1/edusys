from app.enums.class_type import ClassType

class ClassSchedule(object):

    def __init__(self, schedule_id, course_id, semester_id, class_capacity, class_type, class_desc):
        self.__schedule_id = schedule_id
        self.__course_id = course_id
        self.__semester_id = semester_id
        self.__class_capacity = class_capacity
        if isinstance(class_type, ClassType):
            self.__class_type = class_type
        else:
            raise Exception("class_type must be of type ClassType")
        self.__class_desc = class_desc

    def get_schedule_id(self):
        return self.__schedule_id

    def get_course_id(self):
        return self.__course_id

    def get_semester_id(self):
        return self.__semester_id

    def get_class_capacity(self):
        return self.__class_capacity

    def set_class_capacity(self, class_capacity):
        self.__class_capacity = class_capacity

    def get_class_type(self):
        return self.__class_type

    def set_class_type(self, class_type):
        if isinstance(class_type, ClassType):
            self.__class_type = class_type
        else:
            raise Exception("class_type must be of type ClassType")

    def get_class_desc(self):
        return self.__class_desc