from django.test import TestCase
from django.contrib.auth.models import User

from rest_framework.test import APITestCase
from rest_framework import status

from .models import Post


class PostModelTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="dhruv",
            password="12345678"
        )

    def test_create_post(self):

        post = Post.objects.create(
            title="My First Blog",
            content="Learning Django REST Framework",
            author=self.user
        )

        self.assertEqual(
            post.title,
            "My First Blog"
        )

        self.assertEqual(
            post.author,
            self.user
        )

    def test_user_can_have_posts(self):

        Post.objects.create(
            title="Django Post",
            content="Django content",
            author=self.user
        )

        self.assertEqual(
            self.user.posts.count(),
            1
        )


class PostAPITest(APITestCase):

    def setUp(self):

        self.user1 = User.objects.create_user(
            username="user1",
            password="12345678"
        )

        self.user2 = User.objects.create_user(
            username="user2",
            password="12345678"
        )

    def test_user_can_create_post(self):

        self.client.force_authenticate(
            user=self.user1
        )

        data = {
            "title": "User 1 Post",
            "content": "My first post",
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

        self.assertEqual(
            response.data["author"],
            "user1"
        )

    def test_user_can_only_see_own_posts(self):

        Post.objects.create(
            title="User 1 Post",
            content="Post 1",
            author=self.user1
        )

        Post.objects.create(
            title="User 2 Post",
            content="Post 2",
            author=self.user2
        )

        self.client.force_authenticate(
            user=self.user1
        )

        response = self.client.get(
            "/api/posts/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            len(response.data["results"]),
            1
        )

        self.assertEqual(
            response.data["results"][0]["author"],
            "user1"
        )

    def test_user_cannot_modify_other_users_post(self):

        post = Post.objects.create(
            title="User 2 Post",
            content="Post 2",
            author=self.user2
        )

        self.client.force_authenticate(
            user=self.user1
        )

        response = self.client.put(
            f"/api/posts/{post.id}/",
            {
                "title": "Changed",
                "content": "Changed content",
                "published": True
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )