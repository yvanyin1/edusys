from profile_status import ProfileStatus
from user import Administrator, AcademicStaff
from course_profile import CourseProfile
from course_request import CourseRequest
from course_catalog import CourseCatalog
from audience_type import AudienceType

academic_staff = AcademicStaff("John", "Smith",
                               "john.smith", "john.smith@mail.mcgill.ca",
                               "12345")
admin = Administrator("Bob", "Anderson",
                      "bob.anderson", "bob.anderson@mail.mcgill.ca",
                      "23456")

course_1 = CourseProfile(250, "Introduction to Computer Science", "COMP 250", "Stacks, queues, etc.",
                  AudienceType.ADULT, 15, 3.0, ProfileStatus.ACTIVE)
course_2 = CourseProfile(303, "Software Design", "COMP 303", "Design patterns",
                  AudienceType.ADULT, 15, 3.0, ProfileStatus.ACTIVE)

# Fetch from DB
course_catalog = CourseCatalog([course_1])
course_catalog.add_course(course_2)

# course_to_request = Course("Data Science 1", "COMP 335", "Data!", )

# academic_staff.request_course()



