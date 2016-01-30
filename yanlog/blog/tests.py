from datetime import timedelta

from django.contrib.auth import authenticate
from django.test import TestCase
from django.utils import timezone

from blog.models import Post

from .factories import PostFactory, TagFactory, UserFactory


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
        self.post1 = PostFactory(tags=(self.tag1,), created_at=timezone.now())
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
        response = self.client.get('/blog/post/%s/' % self.post1.id)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.tag1.name, response.content)
        self.assertIn(self.post1.title, response.content)
        self.assertIn(self.post1.content, response.content)

    def test_create_post_without_login(self):
        """Test create a post without login"""
        response = self.client.get('/blog/post/create/',
                                   follow=True)
        redirect_to = '/blog/login/?next=/blog/post/create/'
        self.assertRedirects(response, redirect_to)

    def test_create_post(self):
        """Test create a new post"""
        self.client.login(username=self.user.username,
                          password=self.user_password)
        response = self.client.get('/blog/post/create/')
        self.assertEqual(response.status_code, 200)
        new_post = {
            'title': 'Hello world',
            'content': 'This is a test post',
            'created_at': '2015-12-16',
            'tags': [self.tag1.id, self.tag2.id]
        }
        response = self.client.post('/blog/post/create/',
                                    new_post, follow=True)
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
        response = self.client.get('/blog/post/%s/edit/' % self.post1.id,
                                   follow=True)
        redirect_to = '/blog/login/?next=/blog/post/%s/edit/' %\
            self.post1.id
        self.assertRedirects(response, redirect_to)

    def test_edit_post(self):
        """Test edit a post"""
        self.client.login(username=self.user.username,
                          password=self.user_password)
        response = self.client.get('/blog/post/%s/edit/' % self.post1.id)
        self.assertEqual(response.status_code, 200)
        new_post = {
            'title': 'Hello world',
            'content': 'This is a test post',
            'created_at': '2015-12-16',
            'tags': [self.tag1.id, self.tag2.id]
        }
        response = self.client.post('/blog/post/%s/edit/' % self.post1.id,
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
        response = self.client.get('/blog/post/%s/delete/' % self.post1.id,
                                   follow=True)
        redirect_to = '/blog/login/?next=/blog/post/%s/delete/' %\
            self.post1.id
        self.assertRedirects(response, redirect_to)

    def test_delete_post(self):
        """Test delete a post"""
        self.client.login(username=self.user.username,
                          password=self.user_password)
        response = self.client.post('/blog/post/%s/delete/' % self.post1.id,
                                    follow=True)
        redirect_to = '/blog/post/admin/'
        self.assertRedirects(response, redirect_to)
        post = Post.objects.filter(id=self.post1.id)
        self.assertFalse(post)

    def test_change_password_without_login(self):
        """Test change the password without login"""
        response = self.client.get('/blog/account/admin/', follow=True)
        # If the user is not login, hitting change password page will return
        # 404 error rather than redirect to the login page.
        self.assertEqual(response.status_code, 404)

    def test_change_password(self):
        """Test change the password"""
        self.client.login(username=self.user.username,
                          password=self.user_password)
        response = self.client.get('/blog/account/admin/')
        # Make sure the flash message doesn't show.
        self.assertNotContains(response, 'updated')
        new_pass = "new_password"
        new_password = {
            "new_password1": new_pass,
            "new_password2": new_pass,
        }
        response = self.client.post('/blog/account/admin/',
                                    new_password, follow=True)
        self.assertRedirects(response, '/blog/account/admin/')
        self.assertContains(response, 'updated')
        result = authenticate(username=self.user.username, password=new_pass)
        self.assertNotEqual(result, None)

    def test_change_password_two_passwords_not_match(self):
        """Test change password by inputing two different passwords"""
        self.client.login(username=self.user.username,
                          password=self.user_password)
        new_password = {
            "new_password1": "new_password1",
            "new_password2": "new_password2",
        }
        response = self.client.post('/blog/account/admin/', new_password)
        # Should get 200 rather than 301(redirect) as changing password
        # was not successful.
        self.assertEqual(response.status_code, 200)
        # No flash displays.
        self.assertNotContains(response, 'updated')
        # Error message display on the new_password2 field.
        self.assertFormError(response, 'form',
                             'new_password2',
                             'The two password fields didn\'t match.')
        # Password should not be changed.
        result = authenticate(username=self.user.username,
                              password=new_password['new_password1'])
        self.assertEqual(result, None)
        result = authenticate(username=self.user.username,
                              password=new_password['new_password2'])
        self.assertEqual(result, None)

    def test_archive_page(self):
        """Test archive page"""
        response = self.client.get('/blog/archives/')
        self.assertEqual(response.status_code, 200)
        tags = response.context['tags']
        years = response.context['years']
        # num of posts of all tags should be only 1
        map(lambda tag: self.assertEqual(tag['num_posts'], 1), tags)
        tags_set = set([tag['name'] for tag in tags])
        # Both tags should be displayed in the archive page
        self.assertTrue(self.tag1.name in tags_set and
                        self.tag2.name in tags_set)
        self.assertEqual(len(years), 2)  # This year and last year
        # num of posts of each year should be only 1
        map(lambda year: self.assertEqual(year['num_posts'], 1), years)
        years_set = set([int(year['year']) for year in years])
        # Both years should be displayed in the archive page
        post1 = Post.objects.get(id=self.post1.id)
        post2 = Post.objects.get(id=self.post2.id)
        self.assertTrue(post1.created_at.year in years_set and
                        post2.created_at.year in years_set)
