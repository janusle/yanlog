from django.test import TestCase
from django.utils import timezone

from .factories import PostFactory, TagFactory

from datetime import timedelta


class BlogTestCase(TestCase):

    def setUp(self):
        self.tag1 = TagFactory()
        self.tag2 = TagFactory()
        self.post1 = PostFactory(tags=(self.tag1,))
        created_at = timezone.now() - timedelta(days=500)
        self.post2 = PostFactory(tags=(self.tag2,), created_at=created_at)

    def test_index(self):
        """Test visit homepage"""
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.tag1.name, response.content)
        self.assertIn(self.post1.title, response.content)
        self.assertIn(self.post1.content, response.content)

    def test_index_with_tag_specified(self):
        """Test visit homepage by specifying a tag"""
        response = self.client.get('/blog/?tag=%s' % self.tag1.name)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.post1.title, response.content)
        self.assertNotIn(self.post2.title, response.content)

    def test_index_with_year_specified(self):
        """Test visit homepage by specifying a year"""
        this_year = timezone.now().year
        response = self.client.get('/blog/?year=%s' % this_year)
        self.assertIn(self.post1.title, response.content)
        self.assertNotIn(self.post2.title, response.content)


    def test_post(self):
        response = self.client.get('/blog/%s/' % self.post1.id)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.tag1.name, response.content)
        self.assertIn(self.post1.title, response.content)
        self.assertIn(self.post1.content, response.content)
