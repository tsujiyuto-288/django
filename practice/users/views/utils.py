from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from users.forms import *

def do_login(request):
    form = LoginForm(request.POST)
    if not form.is_valid():
        return False,"空欄があります。"

    username = form.cleaned_data["username"]
    password = form.cleaned_data["password"]

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return True,"ログインに成功しました。"
    else:
        return False,"ユーザー名かパスワードが間違っています。"
    
def do_logout(request):
    logout(request)
    return True,"ログアウトしました。"