from django.urls import path
from users.views import mypage,utils,login_and_logout,login_page

urlpatterns = [
    path("mypage", mypage.mypage_open, name="mypage_open"),
    path("open_login_and_logout", login_and_logout.open_login_and_logout, name="open_login_and_logout"),
    path("login_and_logout-login_view", login_and_logout.login_view, name="login_and_logout-login_view"),
    path("login_and_logout-logout_view", login_and_logout.logout_view, name="login_and_logout-logout_view"),
    path("open_login_page", login_page.open_login_page, name="open_login_page"),
    path("login_page-login_view", login_page.login_view, name="login_page-login_view"),
]