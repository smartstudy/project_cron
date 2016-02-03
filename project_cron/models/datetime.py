from datetime import datetime, timedelta


class DateTime:
    FORMAT = '%Y-%m-%d %H:%M'

    def __init__(self, year=None, month=None, day=None, hour=None, minute=None):
        now = datetime.now()
        self._datetime = datetime(year=now.year if year is None else year,
                                  month=now.month if month is None else month,
                                  day=now.day if day is None else day,
                                  hour=now.hour if hour is None else hour,
                                  minute=now.minute if minute is None else minute)

    @staticmethod
    def now():
        return DateTime()

    @staticmethod
    def from_string(dt_string):
        dt = datetime.strptime(dt_string, DateTime.FORMAT)
        return DateTime(year=dt.year, month=dt.month, day=dt.day, hour=dt.hour, minute=dt.minute)

    @property
    def weekday(self):
        return self._datetime.weekday()

    @property
    def date(self):
        return self._datetime.strftime('%Y-%m-%d')

    def before(self, days=0, hours=0, minutes=0):
        self._datetime -= timedelta(days=days, hours=hours, minutes=minutes)

    def after(self, days=0, hours=0, minutes=0):
        self._datetime += timedelta(days=days, hours=hours, minutes=minutes)

    def __gt__(self, other):
        if type(other) is datetime:
            return self._datetime > other
        if type(other) is DateTime:
            return other < self._datetime

        raise TypeError("can't compare '%s' and '%s'" % (type(self).__name__, type(other).__name__))

    def __lt__(self, other):
        if type(other) is datetime:
            return self._datetime < other
        if type(other) is DateTime:
            return other > self._datetime

        raise TypeError("can't compare '%s' and '%s'" % (type(self).__name__, type(other).__name__))

    def __eq__(self, other):
        return not self.__gt__(other) and not self.__lt__(other)

    def __str__(self):
        return self._datetime.strftime(DateTime.FORMAT)
