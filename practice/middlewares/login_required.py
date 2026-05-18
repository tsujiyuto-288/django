from django.shortcuts import redirect


class LoginRequiredMiddleware:
    EXEMPT_PATHS = [
        "/users/login_page-login_view/",
        "/users/open_login_page",
        "/admin",
        ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # ログインしていない場合
        if not request.user.is_authenticated:
            # adminかログインページ以外にアクセスしたら
            if not any(request.path.startswith(path) for path in self.EXEMPT_PATHS):
                # loginページに飛ばす
                return redirect("open_login_page")
            
            
        return self.get_response(request)

