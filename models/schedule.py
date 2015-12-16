from models import DateTime
from utils import logutil
from importlib import import_module


class Schedule:
    def __init__(self, schedule_info):
        self._schedule_info = schedule_info
        self._time_reserved = None

    def reset(self):
        logutil.info(self.name, 'Initialize')
        if self.time == 'Always':
            self._time_reserved = str(DateTime.now())
        else:
            hour = int(self.time[0:2])
            minute = int(self.time[2:4])
            reserved_time = DateTime(hour=hour, minute=minute)
            if reserved_time < DateTime.now():
                reserved_time.after(days=1)

            self._time_reserved = str(reserved_time)

    @property
    def name(self):
        return self._schedule_info['Name']

    @property
    def time(self):
        return self._schedule_info['When']['Time']

    @property
    def weekdays(self):
        return self._schedule_info['When']['Weekdays']

    @property
    def parameters(self):
        return self._schedule_info.get('Parameters', [])

    @property
    def time_reserved(self):
        return DateTime.from_string(self._time_reserved)

    @property
    def actions(self):
        return self._schedule_info['Actions']

    def execute(self):
        if not self.is_reservation_time_passed():
            return False

        self.update_reserved_time()
        if not self.is_valid():
            return False

        return self.execute_actions()

    def execute_actions(self):
        logutil.info(self.name, 'Execute')
        parameters = {}.copy()
        for action in self.actions:
            try:
                module_name, func_name = action['Name'].split('.')
                module = import_module('actions.' + module_name)
                func = getattr(module, func_name)
                parameters = func(dict(list(parameters.items()) + list(action.get('Parameters', {}).items())))
                if parameters is None:
                    parameters = {}.copy()
            except Exception:
                import traceback
                logutil.error(self.name, traceback.format_exc())
                traceback.print_exc()
                logutil.newline()
                return False

        logutil.info(self.name, 'Success')
        logutil.newline()

        return True

    def update_reserved_time(self):
        if self.time == 'Always':
            self._time_reserved = str(DateTime.now())
        else:
            reserved_time = self.time_reserved
            reserved_time.after(days=1)
            self._time_reserved = str(reserved_time)

    def is_valid(self):
        return self.is_job_scheduled_this_weekday()

    def is_job_scheduled_this_weekday(self):
        return DateTime.now().weekday in self.weekdays

    def is_reservation_time_passed(self):
        return self.time_reserved < DateTime.now()
