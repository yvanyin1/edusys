from app.enums.season import Season

class Semester(object):

    def __init__(self, semester_id, season, academic_year, start_date, end_date, registration_deadline, withdrawal_deadline):

        self.__semester_id = semester_id
        if isinstance(season, Season):
            self.__season = season
        else:
            raise Exception("season must be of type Season")
        self.__academic_year = academic_year
        self.__start_date = start_date
        self.__end_date = end_date
        self.__registration_deadline = registration_deadline
        self.__withdrawal_deadline = withdrawal_deadline

    def get_season(self):
        return self.__season

    def set_season(self, season):
        if isinstance(season, Season):
            self.__season = season
        else:
            raise Exception("season must be of type Season")

    def get_academic_year(self):
        return self.__academic_year

    def set_academic_year(self, academic_year):
        if isinstance(academic_year, int):
            self.__academic_year = academic_year
        else:
            raise Exception("academic_year must be of type int")

    def get_start_date(self):
        return self.__start_date

    def set_start_date(self, start_date):
        self.__start_date = start_date

    def get_end_date(self):
        return self.__end_date

    def set_end_date(self, end_date):
        self.__end_date = end_date

    def get_registration_deadline(self):
        return self.__registration_deadline

    def set_registration_deadline(self, registration_deadline):
        self.__registration_deadline = registration_deadline

    def get_withdrawal_deadline(self):
        return self.__withdrawal_deadline

    def set_withdrawal_deadline(self, withdrawal_deadline):
        self.__withdrawal_deadline = withdrawal_deadline
