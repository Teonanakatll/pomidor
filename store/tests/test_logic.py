# from unittest import result

# from django.test import TestCase
from unittest import TestCase, result

from store.logic import operations


class LogicTestCase(TestCase):
    def test_plus(self):
        result = operations(16, 13, '+')
        self.assertEqual(29, result)

    def test_minus(self):
        result = operations(6, 13, '-')
        self.assertEqual(-7, result)

    def test_multiplay(self):
        result = operations(6, 13, '*')
        self.assertEqual(78, result)