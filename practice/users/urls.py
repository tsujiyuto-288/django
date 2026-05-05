from django.urls import path
from users import views


urlpatterns = [
    path("mypage", views.mypage_open, name="mypage_open"),
    path("login", views.test_login, name="login"),
    path("logout", views.test_logout, name="logout"),
    

]