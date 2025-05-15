from app.enums.request_status import RequestStatus

class CourseRequest(object):

    def __init__(self, request_id, requester, course, timestamp):
        self.__request_id = request_id
        self.__requester = requester
        self.__course = course
        self.__status = RequestStatus.SUBMITTED  # will be initialized to DRAFT in case
        self.__timestamp = timestamp

    def set_status(self, status):
        self.__status = status
