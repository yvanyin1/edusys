class ScheduledClassSession(object):

    def __init__(self, session_id, schedule_id, location_id, day_of_week, start_time, end_time,
                 session_type, scheduled_date, seq_no, session_changed_type, flag):

        self.__session_id = session_id
        self.__schedule_id = schedule_id
        self.__location_id = location_id
        self.__day_of_week = day_of_week
        self.__start_time = start_time
        self.__end_time = end_time
        self.__session_type = session_type
        self.__scheduled_date = scheduled_date
        self.__seq_no = seq_no
        self.__session_changed_type = session_changed_type
        self.__flag = flag

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

    def get_session_changed_type(self):
        return self.__session_changed_type

    def set_session_changed_type(self, session_changed_type):
        self.__session_changed_type = session_changed_type

    def get_flag(self):
        return self.__flag

    def set_flag(self, flag):
        self.__flag = flag
