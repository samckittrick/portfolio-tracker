from django.test import TestCase

class TestTest(TestCase):

    def test_test_success(self):
        self.assertEqual(1, 1)

    def test_test_fail(self):
        self.assertEqual(1, 1)
