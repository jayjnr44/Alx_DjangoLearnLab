from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


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
