from django.test import TestCase
from .factories import PageFactory

class HomeTestCase(TestCase):
	def setUp(self):
		self.page = PageFactory(is_display_on_home=True)

	def test_home_page(self):
		response = self.client.get("/")
		self.assertEqual(response.status_code, 200)
		# Make sure that pages with is_display_on_home equaling to true are
		# on the home page
		self.assertIn(self.page.link, response.context['links'])
		self.assertIn(self.page.link, response.content)
