from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Post


class PostAPITests(APITestCase):
    def setUp(self):
        self.author = User.objects.create_user(username="author", password="pass12345")
        self.other_user = User.objects.create_user(username="other", password="pass12345")
        self.post = Post.objects.create(
            title="First Post",
            content="Some content",
            author=self.author,
            status=Post.Status.PUBLISHED,
        )
        self.list_url = reverse("post-list")

    def test_list_posts_is_public(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_post_requires_authentication(self):
        response = self.client.post(
            self.list_url, {"title": "New Post", "content": "Body text"}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_user_can_create_post(self):
        self.client.force_authenticate(user=self.author)
        response = self.client.post(
            self.list_url, {"title": "New Post", "content": "Body text"}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["author"]["username"], "author")

    def test_non_author_cannot_update_post(self):
        self.client.force_authenticate(user=self.other_user)
        url = reverse("post-detail", args=[self.post.id])
        response = self.client.patch(url, {"title": "Hacked title"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_author_can_update_own_post(self):
        self.client.force_authenticate(user=self.author)
        url = reverse("post-detail", args=[self.post.id])
        response = self.client.patch(url, {"title": "Updated title"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Updated title")

    def test_filter_by_status(self):
        Post.objects.create(
            title="Draft Post",
            content="Draft content",
            author=self.author,
            status=Post.Status.DRAFT,
        )
        response = self.client.get(self.list_url, {"status": "draft"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [p["title"] for p in response.data["results"]]
        self.assertIn("Draft Post", titles)
        self.assertNotIn("First Post", titles)
