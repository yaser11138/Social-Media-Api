from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth import PermissionDenied
from social_media_api.blog.models import Subscribe
from social_media_api.blog.services.subscribe import create_subscribe, delete_subscribe
from social_media_api.blog.services.post import create_post
User = get_user_model()


class TestSubscribe(TestCase):

    def setUp(self) -> None:
        self.user1 = User.objects.create_user(email="testemail@gmail.com", password="password")
        self.user2 = User.objects.create_user(email="testemail2@gmail.com", password="password")

    def test_create_subscribe(self):
        sub = create_subscribe(subscriber=self.user1, target_email='testemail2@gmail.com')
        self.assertEqual(sub.subscriber, self.user1)
        self.assertEqual(sub.target, self.user2)
        self.assertTrue(Subscribe.objects.filter(subscriber=self.user1, target=self.user2))

        with self.assertRaises(User.DoesNotExist):
            sub = create_subscribe(self.user1, 'nonexistent@example.com')

    def test_delete_subscribe(self):
        sub = create_subscribe(self.user1, 'testemail2@gmail.com')
        delete_subscribe(uuid=sub.uuid, user=self.user1)
        self.assertFalse(Subscribe.objects.filter(subscriber=self.user1, target=self.user2).exists())

    def test_invalid_delete_subscribe(self):
        sub = create_subscribe(self.user1, 'testemail2@gmail.com')

        with self.assertRaises(PermissionDenied):
            delete_subscribe(uuid=sub.uuid, user=self.user2)


class PostSubscribe(TestCase):

    def setUp(self) -> None:
        self.user1 = User.objects.create_user(email="testemail@gmail.com", password="password")

    def test_create_post(self):
        post = create_post(user=self.user1, title="Test", content="This for Test")
        self.assertEqual(post.author, self.user1)
        self.assertEqual(post.title, "Test")
        self.assertEqual(post.content, "This for Test")
