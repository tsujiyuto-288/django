# Django Form について

## Django Formとは

HTMLの入力フォーム（`<input>`タグ）の生成から、送信されたデータのバリデーションや型変換までをやってくれるdjangoの機能

### 💡 概要・メリット

- **バリデーションルールの使い回しと担保**: 自力で複数箇所にif文を書く必要がなく、一度定義した検証ルールを様々な画面で使い回すことができる。特にモデルと連動させれば（ModelForm）、データベース側で定めた制約（文字数や必須など）を満たしていることをシステム全体で明確に担保できる。
- **データ型の自動変換**: 文字列として送られてきたデータを、Pythonで扱いやすいように自動で整数や日時オブジェクトに変換してくれる。

---

## 1. forms.pyの基本的な書き方

`forms.Form` （または `ModelForm`）を継承してクラスを作成し、必要な入力項目を定義する。

### 💡 内容

- クラスの属性としてフィールド（`CharField` など）を定義する。
- `widget` を引数に使うことで、HTML側に出力される際の属性（class、id、placeholderなど）を直接Python側で指定することができる。

### ✒️ 基本的な書き方

```python
from django import forms

class TestForm(forms.Form):
    # バリデーションの型と、HTML生成時の属性(widget)を定義する
    max_length=10, # 10文字以上は入力できないというバリデーションになる。
    book_title = forms.CharField( # ここのbook_titleがname属性になる
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3 book_title",
                "placeholder": "タイトル",
            }
        )
    )
```

---

## 2. HTMLへの書き方

`views.py` からテンプレート（HTML）へ辞書（context）として渡したフォーム変数を、HTML上に展開する。

### 💡 内容

- 全体を `<form method="POST">` タグで囲んで扱う。
- `{% csrf_token %}` はPOST通信に必要なセキュリティ用のトークン。Ajaxにおける `headers` の役割を果たすもので、必ずformタグのすぐ下に入れる。
- `{{ form.book_title }}` のように書くだけで、`forms.py` で定義した `<input>` タグの大枠が自動生成・配置される。

### ✒️ 基本的な書き方

```html
<!-- JavaScript(AJAX)は書かず、HTMLの中だけでサーバーに送信する仕組み -->
<form method="POST" action="{% url 'django_form_register' %}">
  <!-- セキュリティのためのトークン（必須） -->
  {% csrf_token %}

  <label class="form-label">Django Form テスト</label>

  <!-- forms.pyで設定した入力欄がここに自動展開される -->
  {{ form.book_title }}

  <!-- type="submit"にすることで、ボタン押下時にフォーム内の全データが送信される -->
  <button type="submit" class="btn btn-primary w-100">送信する</button>
</form>
```

---

## 3. views.pyでの受け取り方

ブラウザから送信されたデータをFormインスタンスに流し込み、バリデーションを行ってから安全なデータとして取り出す。

### 💡 内容

- **ステップ1（データの受け取り）**:
  `request.POST` に入っているブラウザからの生データを、`TestForm(request.POST)` のように記述して、まずはフォームクラスに丸ごと流し込んで受け取る。
- **ステップ2（バリデーションの実行）**:
  受け取った生データをいきなり取り出そうとせず、まずは `is_valid()` メソッドを実行してデータがルールを守っているかバリデーションを行う
- **ステップ3（データの抽出・取り出し）**:
  検査を通過して初めて **`.cleaned_data`** という名前の辞書オブジェクトが作られるため、そこからキーを指定して安全なデータを抽出する（取り出す）。
- 送信処理の最後は、画面の更新ボタンによる「データの二重送信」を防ぐため、`render`（その場で現在の画面を描画）ではなく **`redirect`（別のURLへ強制的に移動させ直す命令）** を返すのがセオリー

### ✒️ 基本的な書き方

```python
from django.shortcuts import redirect
from .forms import TestForm

def django_form_register(request):
    # 1. 送信ボタン（POST通信）でデータが送られてきたかを確認
    if request.method == "POST":

        # 2. 送られてきた生のデータをフォームクラスに流し込んで実体化する
        form = TestForm(request.POST)

        # 3. バリデーション（必須や文字数など）を検査する
        if form.is_valid():

            # 4. 安全確認が完了したデータが格納されている辞書(cleaned_data)から値を取り出す
            valid_title = form.cleaned_data["book_title"]

            # ===== DBに保存するなどの処理をここで書く =====
            # 例: Book.objects.create(title=valid_title)
            # ==========================================

            # 5. 処理が終わったら、元の画面へリダイレクト（転送）させて完了
            return redirect("test_open")

    # POST以外でのアクセス（GETによるURL直打ち等）時は、弾いて元の画面へ戻す
    return redirect("test_open")
```

## バリデーションの書き方

modelと同じように書くことができる。

### 例

```python
# 10文字以上はダメ
class TestForm(forms.Form):

    book_title = forms.CharField(
        max_length=9, # これを書けばいい
        choice=TEST_CHOICE
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3 book_title",
                "placeholder": "タイトル",
            }
        ),
    )
```

---

## 5. ModelFormの書き方（モデルからフォームを作成する）

モデルに定義済みのフィールド情報（型・文字数制限・choicesなど）をそのままフォームに引き継いで自動生成する方法。実務ではこちらが一般的に使用される。

### 💡 内容

- `forms.Form` の代わりに `forms.ModelForm` を継承する。
- 内部に `class Meta` を定義し、どのモデルのどのフィールドをフォーム化するかを指定する。
- モデル側で定義している `max_length` や `choices` などのバリデーションルールは、フォーム側に自動で反映されるため二重に書く必要がない。
- `widgets` を辞書形式で指定することで、`forms.Form` と同様にHTML属性（class、placeholderなど）をカスタマイズできる。

### ✒️ forms.pyでの書き方

```python
from django import forms
from accounts.models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book          # どのモデルからフォームを作るか
        fields = ["title", "status"]  # モデルの全フィールドのうち、フォームで使いたいものだけを指定
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control mb-3 book_title",
                    "placeholder": "タイトル(10文字まで)",
                }
            ),
            "status": forms.Select(
                attrs={"class": "form-select mb-3 book_status"}
            ),
        }
```

### 💡 forms.Formとの違い

| 項目 | forms.Form | forms.ModelForm |
|---|---|---|
| フィールド定義 | 手動で一つずつ書く | モデルから自動で引き継がれる |
| バリデーション | 手動で設定する | モデルの制約が自動反映される |
| choices（選択肢） | フォーム側で定義が必要 | モデル側の定義がそのまま使われる |
| DB保存 | 自分でORMを書く | `form.save()` で完結する |

### ✒️ views.pyでの使い方

テンプレートへの渡し方や `is_valid()` の使い方は `forms.Form` と同じ。

```python
from .forms import BookForm

def example_view(request):
    if request.method == "POST":
        form = BookForm(request.POST)

        if form.is_valid():
            # ModelFormでは save() を呼ぶだけでDBに保存できる
            form.save()
            return redirect("test_open")

    else:
        form = BookForm()

    return render(request, "example.html", {"book_form": form})
```

### ✒️ HTMLでの使い方

`forms.Form` と同様に、個別のフィールドを指定して展開する。

```html
<!-- 個別に展開する場合 -->
{{ book_form.title }}   <!-- titleの入力欄 -->
{{ book_form.status }}  <!-- statusの選択欄 -->

<!-- 一括で全フィールドを展開する場合 -->
{{ book_form }}
```
