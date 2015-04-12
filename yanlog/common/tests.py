from django.test import TestCase
from django.test import Client

class HomeTestCase(TestCase):
	def setUp(self):
		self.c = Client()

	def testHomePage(self):
		response = self.c.get("/")
		self.assertEqual(response.status_code, 200)

