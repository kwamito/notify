from django.conf.urls import url
from . import views
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("list/", views.NotesList.as_view(), name="notes-list"),
    path("crud/<int:pk>", views.DetailUpdateDeletNote.as_view(), name="crud"),
    path("search/<str:search>", views.search, name="search"),
]
