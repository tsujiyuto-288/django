from django.shortcuts import redirect


class LoginRequiredMiddleware:
    EXEMPT_PATHS = ["/users/login_and_logout/", "/admin"]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # ログインしていない場合
        if not request.user.is_authenticated:
            # adminかログインページ以外にアクセスしたら
            if not any(request.path.startswith(path) for path in self.EXEMPT_PATHS):
                # loginページに飛ばす
                return redirect("login_and_logout")
            
            
        return self.get_response(request)

