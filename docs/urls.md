# URLについて

## urls.py とは

ブラウザから来た **「URL（住所）」** を見て、**「どのビュー（処理）」** に渡すかを決めるための振り分け表のファイル。

### 💡 概要

- Djangoはリクエストを受けると、まず `urls.py` を上から順に見ていき、URLが一致するパターンを探す。
- 一致するパターンが見つかったら、対応するビューを呼び出す。
- 一致するものがなかった場合は404エラーになる。
- ファイル内には `urlpatterns` というリストが必ず存在し、その中に各URLのルールを並べていく。

---

## path() の基本的な書き方

URL1つ分のルールを定義するための関数。`urlpatterns` のリストの中に並べて使う。

### 💡 概要

- 第1引数に **「URLの文字列」**、第2引数に **「呼び出したいビュー」** を指定する。
- 第3引数には `name="..."` を指定し、URLに名前を付けるのが一般的。テンプレートやリダイレクト先で、この名前を使ってURLを参照できる。
- URL文字列の末尾は **`/` で終える** のがDjangoの慣習。

### ✒️ 基本的な書き方

```python
from django.urls import path
from accounts import views

urlpatterns = [
    # path("URL文字列", ビュー, name="URLの名前")
    path("mypage/", views.mypage_open, name="mypage_open"),
]
```

---

## 関数ビューとクラスビューの登録の違い

### 💡 概要

- **関数ビュー**: 関数名をそのまま渡すだけ。
- **クラスビュー**: クラス名のあとに **`.as_view()`** を付けて渡す必要がある。

### ✒️ 基本的な書き方

```python
from django.urls import path
from accounts import views
from accounts.views import BookListView

urlpatterns = [
    # --- 関数ビューの場合 ---
    path("mypage/", views.mypage_open, name="mypage_open"),

    # --- クラスビューの場合 ---
    # クラス名のあとに必ず .as_view() を付ける
    path("book_list/", BookListView.as_view(), name="book_list_open"),
]
```

---

## name属性について

URLに名前を付けておくことで、テンプレートやビュー内で **「URLそのものの文字列」ではなく「名前」で参照できる** ようになる。

### 💡 概要

- URLは後から変更されることが多いが、`name` を使って参照しておけば、URLの文字列が変わっても **`urls.py` 側を直すだけで済む**。
- テンプレート内では `{% url 'name' %}` という形で使う。
- ビュー内のリダイレクトでは `redirect("name")` という形で使う。

### ✒️ 基本的な書き方

```python
# urls.py
urlpatterns = [
    path("mypage/", views.mypage_open, name="mypage_open"),
]
```

```html
<!-- テンプレート内での使用 -->
<a href="{% url 'mypage_open' %}">マイページへ</a>
```

```python
# ビュー内での使用
from django.shortcuts import redirect

def some_view(request):
    return redirect("mypage_open")
```

---

## include() によるurls.pyの分割

アプリごとに `urls.py` を分けて管理し、プロジェクトの `urls.py` から読み込むための仕組み。

### 💡 概要

- アプリが増えるとプロジェクトの `urls.py` が肥大化するため、**アプリ単位で `urls.py` を分割する** のが一般的。
- プロジェクト側の `urls.py` で `include("アプリ名.urls")` と書くと、そのアプリの `urls.py` を読み込んでくれる。
- `path("accounts/", include("accounts.urls"))` のように書くと、`accounts/` で始まるURLは全てアプリ側の `urls.py` に処理を任せることになる。

### ✒️ 基本的な書き方

```python
# --- プロジェクト側の urls.py ---
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    # accounts/ で始まるURLは、accounts/urls.py に任せる
    path("accounts/", include("accounts.urls")),
]


# --- アプリ側の accounts/urls.py ---
from django.urls import path
from . import views

urlpatterns = [
    # 実際のURLは "accounts/mypage/" になる
    path("mypage/", views.mypage_open, name="mypage_open"),
]
```

---

---

## URLから変数を受け取る（パスコンバータ）

URLの一部を **「変数」として受け取り**、ビューに渡すための書き方。`<型:変数名>` という形でURL内に書く。

### 💡 概要

- `<int:pk>` のように書くと、URLの該当部分が **指定した型に一致した時だけ** マッチし、その値を **変数名（`pk`）に入れた状態でビューを呼び出す** ことができる。
- ビュー側は引数として受け取るだけでよく、URLから値を取り出す処理を自分で書く必要はない。
- 型が一致しないURLは **ビューに到達する前にDjangoが弾いてくれる**（404になる）ため、ビュー側で型チェックをする必要がない。
- DetailViewなど一部の汎用ビューを使う場合、変数名は **`pk` または `slug`** にすることが決まりになっている。

### 💡 よく使う型一覧

| 型     | 意味                                   | マッチする例        |
| ------ | -------------------------------------- | ------------------- |
| `int`  | 0以上の整数                            | `3`, `100`          |
| `str`  | `/` を含まない文字列                   | `hello`, `book-1`   |
| `slug` | 半角英数・ハイフン・アンダースコアのみ | `my-book-1`         |
| `uuid` | UUID形式                               | `550e8400-e29b-...` |
| `path` | `/` を含む文字列                       | `a/b/c`             |

### ✒️ 基本的な書き方

```python
# --- urls.py ---
# <int:pk> の部分にマッチした整数が、変数 pk としてビューに渡される
urlpatterns = [
    path("book/<int:pk>/", views.book_detail, name="book_detail"),
]


# --- views.py（関数ビューの場合） ---
# URLで指定した変数名（pk）が、そのまま引数名になる
def book_detail(request, pk):
    book = Book.objects.get(pk=pk)
    return render(request, "book_detail.html", {"book": book})


# --- views.py（クラスビュー / DetailView の場合） ---
# DetailViewが内部で pk を使って自動でデータを取得してくれる
class BookDetailView(DetailView):
    model = Book
    template_name = "book_detail.html"
```

### 💡 動きの流れ

ユーザーが `/book/3/` にアクセスした時の流れ。

1. Djangoが `<int:pk>` の部分に `3` を当てはめる → `pk=3` が確定
2. 該当のビューが `pk=3` を引数として渡された状態で呼び出される
3. ビュー内では既に `pk` に値が入っているため、そのまま使える

---
