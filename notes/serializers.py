from rest_framework import serializers
from .models import Note
from django.conf import settings
from datetime import datetime


class NoteSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.email")
    notes_count = serializers.ReadOnlyField(source="all_users_notes_count")
    time = serializers.ReadOnlyField(source="timer")

    class Meta:
        model = Note
        fields = [
            "id",
            "title",
            "body",
            "created_at",
            "author",
            "colour",
            "notes_count",
            "time",
        ]
