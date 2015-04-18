from django.test import TestCase
from .factories import PageFactory, SettingFactory

class HomeTestCase(TestCase):
	def setUp(self):
		self.page = PageFactory(is_display_on_home=True)
		self.setting = SettingFactory()

	def test_home_page(self):
		response = self.client.get("/")
		self.assertEqual(response.status_code, 200)
		# Make sure that pages with is_display_on_home equaling to true are
		# on the home page
		self.assertIn(self.page.url, response.context['urls'][0])
		self.assertIn(self.page.url, response.content)

		self.assertEqual(self.setting.github, response.context['github'])
		self.assertEqual(self.setting.twitter, response.context['twitter'])
		self.assertEqual(self.setting.linkedin, response.context['linkedin'])
