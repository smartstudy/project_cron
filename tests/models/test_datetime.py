import unittest

from project_cron.models import DateTime


class TestDateTime(unittest.TestCase):
    def test_init_with_specific_hour(self):
        datetime = DateTime(hour=3)

        self.assertEqual(datetime._datetime.hour, 3)

    def test_to_string(self):
        datetime = DateTime(year=2015, month=11, day=25, hour=16, minute=7)

        self.assertEqual(str(datetime), '2015-11-25 16:07')

    def test_from_string(self):
        datetime = DateTime.from_string('2015-11-25 16:07')

        self.assertEqual(datetime, DateTime(year=2015, month=11, day=25, hour=16, minute=7))
