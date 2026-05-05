from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from users.forms import *


def mypage_open(request):
    user = request.user
    if user.is_authenticated:
        info = "ログイン済み"
    else:
        info = "未ログイン"
    return render(request,"mypage.html",{"user":user,"info":info})

def test_login_open(request):
    login_form = LoginForm()
    return render(request,"login.html",{"login_form":login_form})

def test_logout(request):
    pass