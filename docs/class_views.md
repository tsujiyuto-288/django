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

---

# DetailViewについて

`ListView` の **「単体バージョン」**。あるモデルから **1件だけ** 取得してテンプレートに表示するための汎用クラスベースビュー。

### 💡 概要

- 仕組みも書き方もほとんど `ListView` と同じ。違いは **「複数件取得 → 1件取得」** の部分だけ。
- URLに `<int:pk>` を付けて、その `pk` の値を使って `Model.objects.get(pk=...)` 相当の処理を内部で行う。
- テンプレート側では、デフォルトで **`object`**（単数形）という変数名で1件のデータを受け取れる。

### ✒️ 基本的な書き方

```python
# --- views.py ---
from django.views.generic import DetailView
from .models import Book

class BookDetailView(DetailView):
    model = Book                       # どのモデルから1件取得するか
    template_name = "book_detail.html" # 表示に使うテンプレート
```

### ✒️ urls.pyでの登録

`ListView` と違い、URLに **`<int:pk>`** を付けて、どの1件を取りに行くかを指定する必要がある。

```python
from .views import BookDetailView

urlpatterns = [
    path("book/<int:pk>/", BookDetailView.as_view(), name="book_detail"),
]
```

### ✒️ HTMLでの受け取り方

デフォルトでは **`object`** という変数名で1件のデータが渡される。

```html
<h1>{{ object.title }}</h1>
<p>値段: {{ object.price }}円</p>
```

---

## ListView との違い

### 💡 比較表

| 観点                 | ListView                        | DetailView                         |
| -------------------- | ------------------------------- | ---------------------------------- |
| 取得件数             | 複数件（`Model.objects.all()`） | 1件（`Model.objects.get(pk=...)`） |
| URLにpkが必要か      | 不要                            | **必要**（`<int:pk>/`）            |
| テンプレートの変数名 | `object_list`                   | `object`                           |
| 用途                 | 一覧画面                        | 詳細画面                           |

---

# その他の汎用クラスベースビュー（補足）

### 💡 概要

- `ListView` / `DetailView` の他にも、`CreateView`（新規作成）や `UpdateView`（編集）、`DeleteView`（削除）といった汎用クラスベースビューが用意されている。
- いずれも書き方は `ListView` / `DetailView` と同じノリで、`model` と `template_name` を指定するだけで **ORマッパー（`.objects.create()` など）を自分で書かなくても、フォーム表示・保存・更新・削除までを自動で処理してくれる**。
- ただし `ListView` と同じく、**実務で積極的に使われることは少ない**。複雑な処理が入った瞬間に拡張しづらくなるため、関数ビュー + `ModelForm` で書く方が現場では一般的。
- そのため一旦は **「そういうものがある」** という認識でOK。書き方を細かく覚えるよりも、関数ビュー + `ModelForm` で同じことを書ける力をつける方が応用が利く。

---
