from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework.test import APITestCase, APIRequestFactory, APIClient
from users.models import User
from rest_framework import status
from users.models import Profile, Follow
from rest_framework.authtoken.models import Token


class TestFollowers(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user("boy@email.com", "killmonger")
        self.second_user = User.objects.create_user("test@email.com", "killmonger")
        self.third_user = User.objects.create_user("jeff@email.com", "bannnyioli")
        self.follow_view = reverse("follower")
        self.client = APIClient()

    def test_multiple_followings(self):
        self.client.force_login(user=self.user)
        data = {"id": self.second_user.id}
        response = self.client.post(self.follow_view, data)
        self.assertEqual(response.status_code, 201)

    # def test_user_follow_self(self):
    #     self.client.force_login(user=self.user)
    #     data = {"id": self.user.id}
    #     response = self.client.post(self.follow_view, data)

    def test_multiple_following(self):
        self.client.force_login(user=self.second_user)
        data = {"id": self.user.id}
        response = self.client.post(self.follow_view, data)
        second_response = self.client.post(self.follow_view, data)
        third_response = self.client.post(self.follow_view, data)
        print("")
