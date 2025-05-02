from app.enums.day_of_week import DayOfWeek
from app.enums.session_type import SessionType
from app.enums.session_change_type import SessionChangeType
from app.enums.flag import Flag

class ScheduledClassSession(object):

    def __init__(self, session_id, schedule_id, location_id, day_of_week, start_time, end_time,
                 session_type, scheduled_date, seq_no, session_change_type, flag):

        self.__session_id = session_id
        self.__schedule_id = schedule_id
        self.__location_id = location_id
        if isinstance(day_of_week, DayOfWeek):
            self.__day_of_week = day_of_week
        else:
            raise Exception("day_of_week must be of type DayOfWeek")
        self.__start_time = start_time
        self.__end_time = end_time
        if isinstance(session_type, SessionType):
            self.__session_type = session_type
        else:
            raise Exception("session_type must be of type SessionType")
        self.__scheduled_date = scheduled_date
        self.__seq_no = seq_no
        if isinstance(session_change_type, SessionChangeType) or session_change_type is None:
            self.__session_change_type = session_change_type
        else:
            raise Exception("session_change_type must be of type SessionChangeType")
        if isinstance(flag, Flag):
            self.__flag = flag
        else:
            raise Exception("flag must be of type Flag")

    def get_session_id(self):
        return self.__session_id

    def get_schedule_id(self):
        return self.__schedule_id

    def get_location_id(self):
        return self.__location_id

    def get_day_of_week(self):
        return self.__day_of_week

    def get_start_time(self):
        return self.__start_time

    def get_end_time(self):
        return self.__end_time

    def get_session_type(self):
        return self.__session_type

    def get_scheduled_date(self):
        return self.__scheduled_date

    def get_seq_no(self):
        return self.__seq_no

    def get_session_change_type(self):
        return self.__session_change_type

    def set_session_change_type(self, session_change_type):
        if isinstance(session_change_type, SessionChangeType) or session_change_type is None:
            self.__session_change_type = session_change_type
        else:
            raise Exception("session_change_type must be of type SessionChangeType")

    def get_flag(self):
        return self.__flag

    def set_flag(self, flag):
        if isinstance(flag, Flag):
            self.__flag = flag
        else:
            raise Exception("flag must be of type Flag")
