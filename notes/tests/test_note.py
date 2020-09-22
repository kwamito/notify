from django.test import TestCase
from users.models import User, Profile
from notes.models import Note
from django.urls import reverse
from rest_framework.test import APIClient
import json

# from django_dynamic_fixture import G

# Create your tests here.
class UserNoteTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(email="kwame@email.com", password="nana")
        self.second_user = User.objects.create(email="test@email.com", password="test")
        self.notes_url = reverse("notes-list")
        self.client = APIClient()
        Note.objects.create(
            title="Lorem ipsum something",
            body="the body of lorem ipsum",
            author=self.user,
        )
        Note.objects.create(
            title="Lorem ipsum something",
            body="the body of lorem ipsum",
            author=self.second_user,
        )

    def test_notes_post(self):
        self.client.force_login(user=self.user)
        data = {
            "title": "djfl",
            "body": "djlkasjfjs",
            "colour": "#F1C40F",
        }

        print(data)
        response = self.client.post(self.notes_url, data=data, format="json")
        print(response)

    def test_notes_post_total(self):
        url = reverse("notes-list")
        self.client.force_login(user=self.user)
        response = self.client.get(url)
        notes = Note.objects.filter(author=self.user)
        notes_count = notes.count()
        print(response.data.get("author"))
        # self.assertEqual(notes_count, response.data.notes_count)
