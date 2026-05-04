# ClassViewについて

クラスベースビュー（CBV）は、`View` クラスを継承して定義するビューのこと。関数ビュー（FBV）が1つの関数で全てのHTTPメソッドを処理するのに対し、
CBVは**HTTPメソッドごとにメソッドを分けて書ける**のが大きな特徴。

### 💡 概要

- `django.views` の `View` を継承してクラスを作る。
- クラス内に `get()` `post()` などのメソッドを定義する。
- リクエストが来たとき、Djangoが**HTTPメソッド名と一致するメソッドを自動で呼び出してくれる**ので、関数ビューでよくある `if request.method == "POST":` の分岐が不要になる。

### ✒️ views.pyでの基本的な書き方

```python
from django.views import View
from django.shortcuts import render, redirect

class Test3PageOpen(View):
    # GETリクエストで呼び出されたときの処理
    def get(self, request):
        return render(request, "test3.html", {"page_title": "勉強場3"})

    # POSTリクエストで呼び出されたときの処理
    def post(self, request):
        # フォーム送信時の処理など
        return redirect("test_open")
```

### ✒️ urls.pyでの登録

関数ビューと違い、`.as_view()` を付けて登録する必要がある。

```python
from .views import Test3PageOpen

urlpatterns = [
    path("test3/", Test3PageOpen.as_view(), name="test3_open"),
]
```

### 💡 関数ビューとの比較

| 観点                    | 関数ビュー（FBV）                     | クラスビュー（CBV）                   |
| ----------------------- | ------------------------------------- | ------------------------------------- |
| HTTPメソッドの分岐      | `if request.method == "POST":` で書く | `get()` / `post()` メソッドで自動分岐 |
| urls.pyでの登録         | 関数名をそのまま渡す                  | `.as_view()` を付けて渡す             |
| 同じURLでGET/POSTを処理 | 1つの関数内で分岐させる必要がある     | メソッドが分かれるので見通しが良い    |

### 💡 使いどころ

- **1ページにつき1つのCBVにまとめられる**: 同じURLでGET（画面表示）とPOST（送信処理）の両方を扱えるため、`/form/` と `/form/submit/` のようにURLを2つに分ける必要がなく、関連する処理が1箇所に集まり可読性が上がる。
- **継承で共通処理をまとめて書ける**: 認証チェックや共通のコンテキスト渡しなど、複数のビューで使い回したい処理を親クラスに書いておけば、子クラスはそれを継承するだけで済むのでDRYに書ける。

---

# ListViewについて

Djangoが用意している**汎用クラスベースビュー**の一つで、
「あるモデルの一覧をテンプレートに表示する」という定型処理を、3行ほどの記述だけで実現できるようにしてくれる仕組み。

### 💡 概要

- `model` と `template_name` を指定するだけで、内部的に `Model.objects.all()` の取得 → テンプレートへの受け渡し までを自動で行ってくれる。
- テンプレート側では、デフォルトで `object_list` という変数名で一覧データを受け取れる。
- 関数ビューで書いた場合の以下のような定型処理を、3行で書けるようにしたものに過ぎない。

### ✒️ 関数ビューで書いた場合との比較

```python
# --- 関数ビューで書いた場合 ---
def book_list(request):
    object_list = Book.objects.all()
    return render(request, "book_list.html", {"object_list": object_list})


# --- ListView で書いた場合 ---
class BookListView(ListView):
    model = Book
    template_name = "book_list.html"
```

---

## 基本的な書き方

### 💡 概要

- `django.views.generic` から `ListView` を読み込み、それを継承したクラスを作るだけ。
- `model` と `template_name` の2つを指定するのが最低限の構成。

### ✒️ 基本的な書き方

```python
from django.views.generic import ListView
from .models import Book

class BookListView(ListView):
    model = Book                    # どのモデルから一覧を取得するか
    template_name = "book_list.html"  # 表示に使うテンプレート
```

### ✒️ urls.pyでの登録

クラスベースビューは関数ビューと違い、`.as_view()` を付けてURLに登録する。

```python
from .views import BookListView

urlpatterns = [
    path("books/", BookListView.as_view(), name="book_list"),
]
```

### ✒️ HTMLでの受け取り方

デフォルトでは `object_list` という変数名で一覧データが渡される。

```html
<ul>
  {% for book in object_list %}
  <li>{{ book.title }}</li>
  {% endfor %}
</ul>
```

## 実務での使われ方の実態

### 💡 概要

`ListView` はDjangoの代表的な機能として紹介されることが多いが、**実務では限定的な場面でしか使われない**のが実情。「とりあえず使う」のではなく、「使いどころを見極めて使う」スタンスが現場では一般的らしい。

### 💡 使われる場面

- 単純なCRUD画面（社内管理ツール、admin的な一覧画面など）
- プロトタイプや学習用の簡易画面
- ロジックがほぼなく「モデルを一覧表示するだけ」の画面

### 💡 使われない場面

- 複雑な業務ロジックが入る画面 → 関数ビュー、または素の `View` クラスで書くチームが多い。
- API → そもそもDRF（Django REST Framework）の `ViewSet` を使うため、`ListView` の出番はない。
- 将来的に拡張する可能性がある画面

### 💡 嫌われる理由（拡張性の問題）

- **継承チェーンが深い**: `ListView` の中身は多重継承構造で、どこで何が起きているか追いにくい。
- **拡張するほど読みにくくなる**: `get_queryset` / `get_context_data` / `get_template_names` などメソッドが散らばり、処理の流れが追いづらくなる。
- **関数ビューなら上から下に読めば終わる**: 認知コストが圧倒的に低く、新しく入ったメンバーでも理解しやすい。

### 💡 結論

- 「`ListView`」より「`ListView` がやっていることを関数ビューで書く」方が応用が利くので基本そっちで
