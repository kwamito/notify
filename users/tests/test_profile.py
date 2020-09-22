from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework.test import APITestCase, APIRequestFactory, APIClient
from users.models import User
from rest_framework import status
from users.models import Profile
from rest_framework.authtoken.models import Token


class UserTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user("boy@email.com", "killmonger")
        self.create_url = reverse("user-create-api")
        self.token_url = reverse("token")
        self.token_login = reverse("login")
        self.client = APIClient()

    def test_profile(self):
        self.client.force_login(user=self.user)
        url = reverse("profile-api")
        response = self.client.get(url, format="json")
        print(response)

    def test_profile_patch(self):
        self.client.force_login(user=self.user)
        url = reverse("profile-api")
        data = {"image_url": "http://we.com"}
        response = self.client.patch(url, data=data, format="json")
        profile = Profile.objects.get(user=self.user)
        print(profile.image_url)
        print(response)