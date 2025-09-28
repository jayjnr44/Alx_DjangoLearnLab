from rest_framework.test import APITestCase

class DummyTest(APITestCase):
    def test_dummy(self):
        print("\n🚀 Running tests from the API app!")
        self.assertTrue(True)
    