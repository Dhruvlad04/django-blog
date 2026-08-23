from django.test import TestCase
from django.contrib.auth.models import User

from rest_framework.test import APITestCase
from rest_framework import status

from .models import Post


class PostModelTest(TestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username="dhruv",
            password="12345678"
        )

    def test_create_post(self):
        # Create a post for the user
        post = Post.objects.create(
            title="My First Blog",
            content="Learning Django REST Framework",
            author=self.user
        )

        self.assertEqual(post.title, "My First Blog")
        self.assertEqual(post.author, self.user)

    def test_user_posts_relationship(self):
        # Create a post
        Post.objects.create(
            title="Django Post",
            content="Django content",
            author=self.user
        )

        # Check that the user has one post
        self.assertEqual(self.user.posts.count(), 1)


class PostAPITest(APITestCase):

    def setUp(self):
        # Create first user
        self.user1 = User.objects.create_user(
            username="user1",
            password="12345678"
        )

        # Create second user
        self.user2 = User.objects.create_user(
            username="user2",
            password="12345678"
        )

        # Create a post for user1
        self.post1 = Post.objects.create(
            title="User 1 Post",
            content="Post written by user 1",
            author=self.user1
        )

        # Create a post for user2
        self.post2 = Post.objects.create(
            title="User 2 Post",
            content="Post written by user 2",
            author=self.user2
        )

    def test_unauthenticated_user_can_read_posts(self):
        # No login is done here

        response = self.client.get(
            "/api/posts/"
        )

        # Anyone should be able to read posts
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_authenticated_user_can_create_post(self):
        # Login as user1
        self.client.force_authenticate(
            user=self.user1
        )

        data = {
            "title": "New Post",
            "content": "This is a new post",
            "published": True
        }

        response = self.client.post(
            "/api/posts/",
            data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        # Author should automatically be user1
        self.assertEqual(
            response.data["author"],
            "user1"
        )

    def test_owner_can_update_post(self):
        # Login as the owner
        self.client.force_authenticate(
            user=self.user1
        )

        data = {
            "title": "Updated Post",
            "content": "Updated content",
            "published": True
        }

        response = self.client.put(
            f"/api/posts/{self.post1.id}/",
            data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_user_cannot_update_other_users_post(self):
        # Login as user1
        self.client.force_authenticate(
            user=self.user1
        )

        data = {
            "title": "Trying to change another post",
            "content": "This should not work",
            "published": True
        }

        # post2 belongs to user2
        response = self.client.put(
            f"/api/posts/{self.post2.id}/",
            data
        )

        # User1 should not be allowed
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_owner_can_delete_post(self):
        # Login as the owner
        self.client.force_authenticate(
            user=self.user1
        )

        response = self.client.delete(
            f"/api/posts/{self.post1.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def test_user_cannot_delete_other_users_post(self):
        # Login as user1
        self.client.force_authenticate(
            user=self.user1
        )

        response = self.client.delete(
            f"/api/posts/{self.post2.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_search_posts(self):
        # Search does not require login
        response = self.client.get(
            "/api/posts/?search=User"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_date_filter(self):
        # Test created_at date filter
        date = self.post1.created_at.strftime("%Y-%m-%d")

        response = self.client.get(
            f"/api/posts/?created_at={date}"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_published_filter(self):
        response = self.client.get(
            "/api/posts/?published=true"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )