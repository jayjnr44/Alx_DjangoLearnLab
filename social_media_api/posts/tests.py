from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.utils import timezone
from accounts.models import CustomUser
from posts.models import Post


class FollowFeedTests(APITestCase):
    def setUp(self):
        # Create users
        self.alice = CustomUser.objects.create_user(username="alice", password="pass123")
        self.bob = CustomUser.objects.create_user(username="bob", password="pass123")
        self.carol = CustomUser.objects.create_user(username="carol", password="pass123")

        # Tokens
        self.alice_token = Token.objects.create(user=self.alice)
        self.bob_token = Token.objects.create(user=self.bob)
        self.carol_token = Token.objects.create(user=self.carol)

        # Create posts: bob and carol will make posts
        # Use specific timestamps to assert ordering
        now = timezone.now()
        self.post_b1 = Post.objects.create(author=self.bob, title="Bob 1", content="B1", created_at=now)
        self.post_b2 = Post.objects.create(author=self.bob, title="Bob 2", content="B2", created_at=now + timezone.timedelta(minutes=1))
        self.post_c1 = Post.objects.create(author=self.carol, title="Carol 1", content="C1", created_at=now + timezone.timedelta(minutes=2))

    def auth_header(self, token):
        return {'HTTP_AUTHORIZATION': f'Token {token.key}'}

    def test_follow_unfollow_endpoints(self):
        # Alice follows Bob
        url_follow = reverse('user-follow', kwargs={'pk': self.bob.pk}) \
            if 'user-follow' in [u.name for u in self.client.handler._urls] else None

        # Use viewset action route: /api/accounts/users/{id}/follow/
        follow_route = f"/api/accounts/users/{self.bob.pk}/follow/"
        unfollow_route = f"/api/accounts/users/{self.bob.pk}/unfollow/"

        # Follow
        resp = self.client.post(follow_route, **self.auth_header(self.alice_token))
        # Accept both 200 and 201 depending on implementation
        self.assertIn(resp.status_code, (status.HTTP_200_OK, status.HTTP_201_CREATED))

        # Confirm relationship set at model level
        self.assertTrue(self.alice.is_following(self.bob))
        self.assertIn(self.alice, self.bob.followers.all())

        # Alice unfollows Bob
        resp2 = self.client.post(unfollow_route, **self.auth_header(self.alice_token))
        self.assertIn(resp2.status_code, (status.HTTP_200_OK, status.HTTP_204_NO_CONTENT))
        self.assertFalse(self.alice.is_following(self.bob))

    def test_feed_includes_only_followed_users_posts_and_ordering(self):
        # Initially Alice follows no one -> feed empty
        feed_route = "/api/posts/feed/"

        resp = self.client.get(feed_route, **self.auth_header(self.alice_token))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # If paginated, results are inside 'results'; handle both cases
        data = resp.json()
        results = data.get('results', data)
        self.assertEqual(len(results), 0)

        # Alice follows Bob
        self.client.post(f"/api/accounts/users/{self.bob.pk}/follow/", **self.auth_header(self.alice_token))

        # Now feed should include Bob's posts only (2 posts), ordered newest first (post_b2 then post_b1)
        resp2 = self.client.get(feed_route, **self.auth_header(self.alice_token))
        self.assertEqual(resp2.status_code, status.HTTP_200_OK)
        data2 = resp2.json()
        results2 = data2.get('results', data2)
        # Expect 2 posts (bob's)
        self.assertEqual(len(results2), 2)
        titles = [p.get('title') for p in results2]
        # newest first: "Bob 2" then "Bob 1"
        self.assertEqual(titles, ["Bob 2", "Bob 1"])

        # Alice follows Carol too -> feed should have 3 posts, ordered by created_at descending (Carol 1 newest)
        self.client.post(f"/api/accounts/users/{self.carol.pk}/follow/", **self.auth_header(self.alice_token))
        resp3 = self.client.get(feed_route, **self.auth_header(self.alice_token))
        self.assertEqual(resp3.status_code, status.HTTP_200_OK)
        data3 = resp3.json()
        results3 = data3.get('results', data3)
        self.assertEqual(len(results3), 3)
        titles3 = [p.get('title') for p in results3]
        # newest is Carol 1, then Bob 2, then Bob 1
        self.assertEqual(titles3, ["Carol 1", "Bob 2", "Bob 1"])

    def test_feed_requires_authentication(self):
        feed_route = "/api/posts/feed/"
        resp = self.client.get(feed_route)  # no auth
        # Should be 401 Unauthorized or 403 depending on your view permission
        self.assertIn(resp.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))
