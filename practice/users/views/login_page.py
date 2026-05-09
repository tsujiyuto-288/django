from django.shortcuts import render
from users.views import utils
from django.http import JsonResponse
from users.forms import *


def open_login_page(request):
    login_form = LoginForm()
    return render(request, "login_page.html", {"page_title": "ログインページ","login_form": login_form})

def login_view(request):
    status,message = utils.do_login(request)
    return JsonResponse({"status":status,"message":message})