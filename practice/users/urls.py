from django.urls import path
from users import views


urlpatterns = [
    path("mypage", views.mypage_open, name="mypage_open"),
    path("login_and_logout", views.TestLoginAndLogout.as_view(), name="login_and_logout"),
    path("logout", views.test_logout, name="logout"),
]