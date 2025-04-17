from audience_type import AudienceType
from course import Course

class CourseCatalog(object):

    _instance = None
    _initialized = False

    def __new__(cls, courses=None):  # Singleton pattern
        if cls._instance is None:
            cls._instance = object.__new__(cls)
            # cls._instance.__courses = set(courses) if courses is not None else set()
        return cls._instance

    def __init__(self, courses=None):
        if not self.__class__._initialized:
            self.__courses = set(courses) if courses is not None else set()
            self.__class__._initialized = True

    def get_courses(self):
        return self.__courses.copy()

    def add_course(self, course):
        self.__courses.add(course)

    def remove_course(self, course):
        if course in self.get_courses():
            self.__courses.remove(course)
        else:
            raise Exception('Course not found')


if __name__ == '__main__':
    catalog1 = CourseCatalog([Course("Calculus 1", "MATH 211", "Limits and derivatives",
                                     AudienceType.YOUTH, 15, 3.0)])
    print(catalog1.get_courses())
    catalog2 = CourseCatalog([Course("Calculus 2", "MATH 212", "Integrals",
                                     AudienceType.YOUTH, 15, 3.0)])
    print(catalog2.get_courses())
    print(catalog1 is catalog2)