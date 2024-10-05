from django.test import TestCase
from django.contrib.auth import get_user_model
from social_media_api.blog.models import Post, Subscribe
from social_media_api.blog.selectors.post import get_post, post_list

User = get_user_model()


class PostTest(TestCase):

    def setUp(self):
        # Create two users
        self.user1 = User.objects.create_user(email='user1@example.com', password='password1')
        self.user2 = User.objects.create_user(email='user2@example.com', password='password2')
        self.user3 = User.objects.create_user(email='user3@example.com', password='password3')

        # Create relationships (user1 Subscribes user2)
        Subscribe.objects.create(subscriber=self.user1, target=self.user2)

        # Create posts for user2 and user3
        self.post1 = Post.objects.create(author=self.user2, slug='post-1', content='Content 1')
        self.post2 = Post.objects.create(author=self.user3, slug='post-2', content='Content 2')

    def test_get_post(self):
        post = get_post(slug='post-1')
        self.assertEqual(post, self.post1)

    def test_post_list(self):
        filters = {}
        posts = post_list(filters=filters, user=self.user1)
        self.assertIn(self.post1, posts.qs)  # Ensure user1 sees posts from user2
        self.assertNotIn(self.post2, posts.qs)  # Ensure user1 doesn't see posts from user3

        # Test post list for a user with no Subscribe users
        posts = post_list(filters=filters, user=self.user3)  # user3 has not Subscribed anyone
        self.assertFalse(posts.qs.exists())  # Should return no posts
