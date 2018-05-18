import unittest

from eduserver.controller import Controller
from eduserver.db import Result
from eduserver.db_controller import DBController
from datetime import datetime

from eduserver.filter import Filter


class TestController(unittest.TestCase):
    db_controller = DBController()
    controller = Controller()
    start = datetime.strptime('Jun 1 2018  1:33PM', '%b %d %Y %I:%M%p')
    end = datetime.strptime('Jun 30 2018  1:33PM', '%b %d %Y %I:%M%p')
    min = 0.5
    max = 1
    filter = Filter(start, end, min, max)
    result1 = Result("test_user", 0.1, datetime.strptime('Jul 30 2018  1:33PM', '%b %d %Y %I:%M%p'))
    result2 = Result("test_user", 1, datetime.strptime('Feb 22 2018  1:33PM', '%b %d %Y %I:%M%p'))
    result3 = Result("test_user", 0.8, datetime.strptime('Jun 25 2018  1:33PM', '%b %d %Y %I:%M%p'))
    results = []

    @classmethod
    def setUpClass(self):
        self.results.append(self.result1)
        self.results.append(self.result2)
        self.results.append(self.result3)


    def test_filter_by_date(self):
        actual = self.controller.filter_by_date(self.results, self.start, self.end)
        exptected = []
        exptected.append(self.result3)
        self.assertEqual(exptected, actual)

    def test_filter_by_date_start_is_later(self):
        filter = Filter(self.end, self.start, self.min, self.max)
        with self.assertRaises(Exception) as cm:
            self.controller.get_results_by_filter(filter)
        err = cm.exception
        self.assertEqual(str(err), "Start can't be later than end!")

    def test_filter_by_date_none(self):
        filter = Filter(None, None, self.min, self.max)
        with self.assertRaises(Exception) as cm:
            self.controller.get_results_by_filter(filter)
        err = cm.exception
        self.assertEqual(str(err), "Start and end date can't be empty!")

    def test_filter_by_results(self):
        actual = self.controller.filter_by_results(self.results, self.min, self.max)
        exptected = []
        exptected.append(self.result2)
        exptected.append(self.result3)
        self.assertEqual(exptected, actual)

    def test_filter_by_result_reverse_order(self):
        actual = self.controller.filter_by_results(self.results, self.max, self.min)
        exptected = []
        exptected.append(self.result2)
        exptected.append(self.result3)
        self.assertEqual(exptected, actual)

    def test_filter_by_result_none(self):
        filter = Filter(self.start, self.end, None, None)
        with self.assertRaises(Exception) as cm:
            self.controller.get_results_by_filter(filter)
        err = cm.exception
        self.assertEqual(str(err), "Min and max can't be empty!")