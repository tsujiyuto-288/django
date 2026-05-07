# 認証系についてまとめたmdファイル

## authenticate() について

ユーザー名とパスワードの組み合わせが正しいかをデータベースに照会するメソッド。

### 💡 内容

- 引数で受け取った `username` と `password` の組み合わせが、`auth_user` テーブルに存在するかを調べる。
- **一致するユーザーがいた場合は、そのユーザーの `User` オブジェクトを返す。**
- **一致しなかった場合は `None` を返す。**
- この時点ではまだログイン状態にはならない。あくまで「正しいかどうか」を判定するだけ。

### ✒️ 基本的な書き方

```python
from django.contrib.auth import authenticate

# ユーザー名とパスワードを渡して照会する
user = authenticate(request, username=username, password=password)

# 一致した場合：Userオブジェクトが入っている
# 一致しなかった場合：Noneが入っている
if user is not None:
    # 認証成功時の処理
    pass
else:
    # 認証失敗時の処理
    pass
```

---

## login() について

`authenticate()` で取得した `User` オブジェクトを使って、実際にログイン状態にするメソッド。

### 💡 内容

- 引数に `request` と `User` オブジェクトを渡すことでログイン状態にできる。
- ログインが完了すると、それ以降のリクエストでは `request.user` から、ログイン中のユーザー情報を取得できるようになる。

### ✒️ 基本的な書き方

```python
from django.contrib.auth import authenticate, login

user = authenticate(request, username=username, password=password)

if user is not None:
    # ここでログイン状態になる
    login(request, user)
```

---

## logout() について

ログイン中のユーザーをログアウト状態にするメソッド。

### 💡 内容

- 引数に `request` を渡すだけでログアウトできる。
- ログインの時のように `authenticate()` で照合してから… のような手順は不要。1行で完結する。

### ✒️ 基本的な書き方

```python
from django.contrib.auth import logout

# これだけでログアウトできる
logout(request)
```

---

## ログイン必須ページの保護（@login_required / LoginRequiredMixin）

未ログインのユーザーがアクセスした時、自動でログインページにリダイレクトさせるための仕組み。

### 💡 内容

- **関数ベースビュー（FBV）の場合は `@login_required` デコレータを付ける。**
- **クラスベースビュー（CBV）の場合は `LoginRequiredMixin` を継承する。**
- 未ログイン状態でアクセスされた場合、`settings.py` の `LOGIN_URL` で指定したパスに自動でリダイレクトされる。
- 保護したいビューに対して**1つずつ付与する必要がある**。

### ✒️ 基本的な書き方

```python
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

# --- 関数ベースビュー（FBV）の場合 ---
@login_required
def mypage_open(request):
    ...


# --- クラスベースビュー（CBV）の場合 ---
class MyPageView(LoginRequiredMixin, View):
    def get(self, request):
        ...
```

`settings.py` 側でリダイレクト先を指定しておく：

```python
# settings.py
LOGIN_URL = "/users/login"
```

---
