from django.test import TestCase

from .factories import CategoryFactory, TagFactory, PostFactory

class BlogTestCase(TestCase):

    def setUp(self):
        self.category1 = CategoryFactory()
        self.category2 = CategoryFactory()
        self.tag1 = TagFactory()
        self.tag2 = TagFactory()
        self.post1 = PostFactory(tags=(self.tag1,),
                                 category=self.category1,
                                 lang="en")
        self.post2 = PostFactory(tags=(self.tag2,),
                                 category=self.category2,
                                 lang="cn")

    def test_index(self):
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.category1.name, response.content)
        self.assertIn(self.tag1.name, response.content)
        self.assertIn(self.post1.title, response.content)
        self.assertIn(self.post1.content, response.content)
        # We only display English post in IndexView
        self.assertNotIn(self.post2.title, response.content)

    def test_index_with_category_specified(self):
        response = self.client.get('/blog/?category=%s' % self.category1.name) 
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.post1.title, response.content)
        self.assertNotIn(self.post2.title, response.content)

    def test_index_with_tag_specified(self):
        response = self.client.get('/blog/?tag=%s' % self.tag1.name) 
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.post1.title, response.content)
        self.assertNotIn(self.post2.title, response.content)

    def test_post(self):
        response = self.client.get('/blog/%s/' % self.post1.id)
        self.assertEqual(response.status_code, 200) 
        self.assertIn(self.category1.name, response.content)
        self.assertIn(self.tag1.name, response.content) 
        self.assertIn(self.post1.title, response.content) 
        self.assertIn(self.post1.content, response.content) 
