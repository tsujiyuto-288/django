from django.shortcuts import render

def mypage_open(request):
    user = request.user
    if user.is_authenticated:
        info = "ログイン済み"
    else:
        info = "未ログイン"
    return render(request, "mypage.html", {"user": user, "info": info})