from django.test import TestCase
from django.test import Client
from .factories import PageFactory 

class HomeTestCase(TestCase):
	def setUp(self):
		self.c = Client()
		self.page = PageFactory(is_display_on_home=True)

	def testHomePage(self):
		response = self.c.get("/")
		self.assertEqual(response.status_code, 200)
        self.assertIn(self.page.link, response.content)
