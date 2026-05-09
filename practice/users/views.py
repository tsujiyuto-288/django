from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from users.forms import *
from django.contrib.auth.decorators import login_required


def mypage_open(request):
    user = request.user
    if user.is_authenticated:
        info = "ログイン済み"
    else:
        info = "未ログイン"
    return render(request, "mypage.html", {"user": user, "info": info})


class TestLoginAndLogout(View):
    def get(self, request):
        login_form = LoginForm()
        return render(request, "login_and_logout.html", {"login_form": login_form})

    def post(self, request):
        form = LoginForm(request.POST)
        if not form.is_valid():
            return JsonResponse(
                {"status": "error", "message": "入力内容に不備があります"}
            )

        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({"status": "success"})
        else:
            return JsonResponse(
                {
                    "status": "error",
                    "message": "ユーザー名かパスワードが間違っています。",
                }
            )


def test_logout(request):
    logout(request)
    return JsonResponse({"status": "success"})
