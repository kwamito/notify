from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework.test import APITestCase, APIRequestFactory, APIClient
from users.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token


class UserTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user("boy@email.com", "killmonger")
        self.create_url = reverse("user-create-api")
        self.token_url = reverse("token")
        self.token_login = reverse("login")
        self.client = APIClient()

    def test_create(self):
        data = {"email": "man@email.com", "password": "killmongerishere"}
        response = self.client.post(self.create_url, data, format="json")
        user = User.objects.get(email="man@email.com")
        users = User.objects.all()
        token = Token.objects.get(user=user)
        print(response.data["token"])
        self.assertEqual(response.data["token"], token.__str__())

    def test_login(self):
        url = reverse("login")
        url = "/users/login/"
        data = {"email": "boy@email.com", "password": "killmonger"}
        response = self.client.post(url, data, format="json")
        print(response)

    # def test_login_token(self):
    #     data = {"email": self.user.email, "password": "killmonger"}
    #     response = self.client.post(self.token_url, data=data, format="json")
    #     print(response)
