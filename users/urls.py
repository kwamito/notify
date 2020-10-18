from django.conf.urls import url
from . import views
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    url("api/users", views.UserCreate.as_view(), name="user-create-api"),
    path("api/users-list", views.UserList.as_view(), name="users-list"),
    path("api-token-auth", views.CustomAuthToken.as_view(), name="token"),
    path("api-auth/", include("rest_framework.urls")),
    path("api-login/", obtain_auth_token, name="api-login"),
    path("login/", views.LoginApiView.as_view(), name="login"),
    path("profile/", views.ProfileApiView.as_view(), name="profile-api"),
    path("followers", views.FollowerAPIView.as_view(), name="follower"),
    path("search/<str:search>", views.search, name="user-search"),
]
