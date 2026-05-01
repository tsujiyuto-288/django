# ミドルウェアについて

## ミドルウェアとは

ブラウザからのリクエストがビュー（`views.py`）に届く前と、ビューが返したレスポンスがブラウザに戻る前の**間に挟まって毎回走る共通処理**のこと。

### 💡 概要

- ブラウザからのリクエストは、いきなりビューに届くのではなく、**ミドルウェアの層を上から順に通過してからビューに届く**。
- ビューが返したレスポンスも、**下から順にミドルウェアを通過してからブラウザに戻る**。
- 「全リクエストに横断的に適用したい処理」を、ビューに書かずに一箇所にまとめておくための仕組み。
- すべてのリクエストで毎回走るため、「全画面で共通して必要な処理」だけを書くのが原則。

### ✒️ イメージ図

```
ブラウザ
  ↓ リクエスト
[ミドルウェア1]   ← 行きの処理
[ミドルウェア2]
[ミドルウェア3]
  ↓
views.py（本来の処理）
  ↓ レスポンス
[ミドルウェア3]   ← 帰りの処理
[ミドルウェア2]
[ミドルウェア1]
  ↓
ブラウザ
```

---

## settings.py での定義

### 💡 概要

- ミドルウェアは `settings.py` の **`MIDDLEWARE`** というリストにクラスのパスを並べて登録する。
- リストの**並び順がそのまま処理の順番**になる。上から順にリクエストを処理し、下から順にレスポンスを処理する。
- Djangoプロジェクトを作成した時点で、よく使われるミドルウェアがデフォルトで登録されている。

### ✒️ 基本的な書き方

```python
# settings.py
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
```

---

## デフォルトで登録されている主なミドルウェア

### 💡 概要

普段意識せずに使っている `request.user` や `{% csrf_token %}` などの機能は、これらのミドルウェアが裏で毎回動いてくれているおかげで成立している。

| ミドルウェア               | 主な役割                                                                              |
| -------------------------- | ------------------------------------------------------------------------------------- |
| `SecurityMiddleware`       | HTTPSへのリダイレクトやセキュリティ用ヘッダの付与など、セキュリティ周りの基本処理。   |
| `SessionMiddleware`        | セッション情報の読み書き。これが動いているおかげで `request.session` が使える。       |
| `CsrfViewMiddleware`       | POST通信のCSRFトークンを検証する。`{% csrf_token %}` の検証もこのミドルウェアが行う。 |
| `AuthenticationMiddleware` | ログイン中のユーザー情報を `request.user` にセットする。                              |
| `MessageMiddleware`        | フラッシュメッセージ機能（`messages.success(...)` など）を有効にする。                |
| `XFrameOptionsMiddleware`  | `<iframe>` での表示を制限し、クリックジャッキング攻撃を防ぐ。                         |

### 💡 補足

- `request.user` がビュー内で当たり前のように使えるのは、`AuthenticationMiddleware` がリクエスト到達前に毎回ユーザー情報をセットしてくれているから。
- HTML側で `{{ user.username }}` のようにテンプレートタグから直接ユーザー情報が参照できるのも、ミドルウェア経由でリクエストにユーザー情報が積まれているおかげ。

---

## 現時点での理解の目安

### 💡 概要

- ミドルウェアは「リクエストとレスポンスの間に挟まって、毎回走る共通処理」というイメージを持っておけばOK。
- 現時点では自分でミドルウェアを自作する場面はほぼないため、まずは **`settings.py` の `MIDDLEWARE` に登録されているものが、リクエストのたびに毎回走っているんだな** という認識でよい。
- `request.user` が使えたり、テンプレートでログインユーザーの情報が取れたりするのは、デフォルトのミドルウェアのおかげ、というところまで押さえられていれば十分。
