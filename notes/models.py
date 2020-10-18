from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from datetime import datetime
from .time import determine_time


# Create your models here.
class Note(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=80)
    body = models.TextField()
    COLOURS = [
        ("#F1C40F", "Dark Orange"),
        ("#CD5C5C", "Indian Red"),
        ("#F08080", "Light Coral"),
        ("#000000", "Black"),
        ("#FFFF00", "Yellow"),
        ("#FF00FF", "Fuschia"),
        ("#C0C0C0", "Silver"),
    ]

    colour = models.CharField(choices=COLOURS, max_length=25, default="#C0C0C0")
    created_at = models.DateTimeField(auto_now_add=True)
    is_private = models.BooleanField(default=False, null=True, blank=True)

    def all_users_notes_count(self):
        filtered_notes = Note.objects.filter(author=self.author)
        notes_count = filtered_notes.count()
        return notes_count

    def timer(self):
        return determine_time(self.created_at)