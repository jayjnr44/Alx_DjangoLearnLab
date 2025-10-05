from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post, Comment
from django.urls import reverse


class AuthTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass", email="test@example.com"
        )

    def test_login(self):
        response = self.client.post(
            reverse("login"), {"username": "testuser", "password": "testpass"}
        )
        self.assertEqual(response.status_code, 302)  # Redirects on success

    def test_logout(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(reverse("logout"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Logged out", status_code=200)

    def test_register(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "newuser",
                "email": "new@example.com",
                "password1": "newpass123",
                "password2": "newpass123",
            },
        )
        self.assertEqual(response.status_code, 302)  # Redirects on success
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_profile_edit(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(
            reverse("profile"),
            {
                "email": "updated@example.com",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "updated@example.com")


class CommentTests(TestCase):
    def setUp(self):
        # create two users and a post
        self.user = User.objects.create_user(
            username="commenter", password="pass123", email="c@example.com"
        )
        self.other = User.objects.create_user(
            username="other", password="pass456", email="o@example.com"
        )
        self.post = Post.objects.create(title="T", content="C", author=self.user)

    def test_create_comment_requires_login(self):
        url = reverse("comment-create", kwargs={"post_pk": self.post.pk})
        response = self.client.post(url, {"content": "Hello"})
        # should redirect to login
        self.assertEqual(response.status_code, 302)

    def test_create_comment(self):
        self.client.login(username="commenter", password="pass123")
        url = reverse("comment-create", kwargs={"post_pk": self.post.pk})
        response = self.client.post(url, {"content": "Nice post"})
        # after creation, should redirect to post-detail
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Comment.objects.filter(
                post=self.post, content__icontains="Nice post"
            ).exists()
        )

    def test_comment_edit_by_author(self):
        # author creates comment
        comment = Comment.objects.create(
            post=self.post, author=self.user, content="orig"
        )
        self.client.login(username="commenter", password="pass123")
        url = reverse("comment-update", kwargs={"pk": comment.pk})
        response = self.client.post(url, {"content": "edited"})
        self.assertEqual(response.status_code, 302)
        comment.refresh_from_db()
        self.assertEqual(comment.content, "edited")

    def test_comment_edit_by_other_forbidden(self):
        comment = Comment.objects.create(
            post=self.post, author=self.user, content="orig"
        )
        self.client.login(username="other", password="pass456")
        url = reverse("comment-update", kwargs={"pk": comment.pk})
        response = self.client.post(url, {"content": "hacked"})
        # should be forbidden or redirect (UserPassesTestMixin typically returns 403)
        self.assertIn(response.status_code, (302, 403))
        comment.refresh_from_db()
        self.assertEqual(comment.content, "orig")

    def test_comment_delete_by_author(self):
        comment = Comment.objects.create(
            post=self.post, author=self.user, content="to delete"
        )
        self.client.login(username="commenter", password="pass123")
        url = reverse("comment-delete", kwargs={"pk": comment.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Comment.objects.filter(pk=comment.pk).exists())

    def test_comment_delete_by_other_forbidden(self):
        comment = Comment.objects.create(
            post=self.post, author=self.user, content="to delete"
        )
        self.client.login(username="other", password="pass456")
        url = reverse("comment-delete", kwargs={"pk": comment.pk})
        response = self.client.post(url)
        self.assertIn(response.status_code, (302, 403))
        self.assertTrue(Comment.objects.filter(pk=comment.pk).exists())
