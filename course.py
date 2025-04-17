from audience_type import AudienceType

class Course(object):

    def __init__(self, name, code, description, target_audience, duration_in_weeks, number_of_credits):
        self.__name = name
        self.__code = code
        self.__description = description
        if isinstance(target_audience, AudienceType):
            self.__target_audience = target_audience
        else:
            raise Exception("target_audience must be of type AudienceType")
        self.__target_audience = target_audience
        self.__duration_in_weeks = duration_in_weeks
        self.__credits = number_of_credits

    def __eq__(self, other):
        if not isinstance(other, Course):
            return False
        return self.__name == other.__name and self.__code == other.__code

    def __hash__(self):
        return hash((self.__code, self.__name))

    def __repr__(self):
        return (f"Course({self.__name}, {self.__code}, {self.__description}, " +
                f"{self.__target_audience}, {self.__duration_in_weeks}, {self.__credits})")

    def __str__(self):
        return f"{self.__code}: {self.__name}"

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def get_code(self):
        return self.__code

    def set_code(self, code):
        self.__code = code

    def get_description(self):
        return self.__description

    def set_description(self, description):
        self.__description = description

    def get_target_audience(self):
        return self.__target_audience

    def set_target_audience(self, target_audience):
        if isinstance(target_audience, AudienceType):
            self.__target_audience = target_audience
        else:
            raise Exception("target_audience must be of type AudienceType")

    def get_duration_in_weeks(self):
        return self.__duration_in_weeks

    def set_duration_in_weeks(self, duration_in_weeks):
        self.__duration_in_weeks = duration_in_weeks

    def get_credits(self):
        return self.__credits

    def set_credits(self, number_of_credits):
        self.__credits = number_of_credits


if __name__ == '__main__':
    course_1 = Course("Introduction to Computer Science", "COMP 250", "Stacks, queues, etc.",
                      AudienceType.ADULT, 15, 3.0)
    course_2 = Course("Introduction to Computer Science", "COMP 250", "Recurrences",
                      AudienceType.YOUTH, 15, 3.0)
    print(course_1.__dict__)
    print(course_1 == course_2)