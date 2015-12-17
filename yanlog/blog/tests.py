from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from accounts.factories import UserFactory
from blog.models import Post

from .factories import PostFactory, TagFactory


class BlogTestCase(TestCase):

    def setUp(self):
        # Create a test user
        self.user_password = 'abc'
        self.user = UserFactory(username='bender')
        self.user.set_password(self.user_password)
        self.user.save()
        # Create tags
        self.tag1 = TagFactory()
        self.tag2 = TagFactory()
        # Create posts
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

    def test_visit_post(self):
        """Test visit a post"""
        response = self.client.get('/blog/%s/' % self.post1.id)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.tag1.name, response.content)
        self.assertIn(self.post1.title, response.content)
        self.assertIn(self.post1.content, response.content)

    def test_create_post_without_login(self):
        """Test create a post without login"""
        response = self.client.get('/blog/create/',
                                   follow=True)
        redirect_to = '/accounts/login/?next=/blog/create/'
        self.assertRedirects(response, redirect_to)

    def test_create_post(self):
        """Test create a new post"""
        self.client.login(username=self.user.username,
                          password=self.user_password)
        response = self.client.get('/blog/create/')
        self.assertEqual(response.status_code, 200)
        new_post = {
            'title': 'Hello world',
            'content': 'This is a test post',
            'created_at': '2015-12-16',
            'tags': [self.tag1.id, self.tag2.id]
        }
        response = self.client.post('/blog/create/', new_post, follow=True)
        post = Post.objects.filter(title=new_post['title'])
        self.assertTrue(post)  # Ensure the post is existed.
        post = post[0]
        self.assertEqual(post.title, new_post['title'])
        self.assertEqual(post.content, new_post['content'])
        self.assertEqual(post.created_at.strftime('%Y-%m-%d'),
                         new_post['created_at'])
        self.assertIn(self.tag1, post.tags.all())
        self.assertIn(self.tag2, post.tags.all())
        self.assertRedirects(response, post.get_absolute_url())

    def test_edit_post_without_login(self):
        """Test edit a post without login"""
        response = self.client.get('/blog/%s/edit/' % self.post1.id,
                                   follow=True)
        redirect_to = '/accounts/login/?next=/blog/%s/edit/' % self.post1.id
        self.assertRedirects(response, redirect_to)

    def test_edit_post(self):
        """Test edit a post"""
        self.client.login(username=self.user.username,
                          password=self.user_password)
        response = self.client.get('/blog/%s/edit/' % self.post1.id)
        self.assertEqual(response.status_code, 200)
        new_post = {
            'title': 'Hello world',
            'content': 'This is a test post',
            'created_at': '2015-12-16',
            'tags': [self.tag1.id, self.tag2.id]
        }
        response = self.client.post('/blog/%s/edit/' % self.post1.id,
                                    new_post, follow=True)
        post = Post.objects.get(id=self.post1.id)
        self.assertEqual(post.title, new_post['title'])
        self.assertEqual(post.content, new_post['content'])
        self.assertEqual(post.created_at.strftime('%Y-%m-%d'),
                         new_post['created_at'])
        self.assertIn(self.tag1, post.tags.all())
        self.assertIn(self.tag2, post.tags.all())
        self.assertRedirects(response, post.get_absolute_url())

    def test_delete_post_without_login(self):
        """Test delete a post without login"""
        response = self.client.get('/blog/%s/delete/' % self.post1.id,
                                   follow=True)
        redirect_to = '/accounts/login/?next=/blog/%s/delete/' % self.post1.id
        self.assertRedirects(response, redirect_to)

    def test_delete_post(self):
        """Test delete a post"""
        self.client.login(username=self.user.username,
                          password=self.user_password)
        response = self.client.post('/blog/%s/delete/' % self.post1.id,
                                    follow=True)
        redirect_to = '/blog/admin/'
        self.assertRedirects(response, redirect_to)
        post = Post.objects.filter(id=self.post1.id)
        self.assertFalse(post)
