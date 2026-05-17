# Django テストについて

## Djangoテストの基本

Djangoには「ビューが想定通りに動いているか」を自動でチェックするための仕組みが用意されている。`django.test.TestCase` を継承したクラスを作り、その中にテストメソッドを書いていくのが基本。

### 💡 概要・メリット

- **手動確認の自動化**: ブラウザで一つ一つアクセスして確認する代わりに、コードで一気に検証ができる。
- **デグレ検知**: コードを編集したときに、別の場所が壊れていないかを素早く確認できる。
- **`TestCase` を継承するだけで `self.client`（テスト用クライアント）や `self.assert〜` 系メソッドが使えるようになる。**
- テスト対象は「ステータスコード」「使われたテンプレート」「テンプレートに渡されたデータ（context）」など。

### ✒️ 基本的な書き方

```python
from django.test import TestCase
from django.urls import reverse

class BookTestCase(TestCase):
    def test_book_list_page_returns_200(self):
        # URLを名前から解決
        url = reverse("book_list_open")

        # テスト用クライアントでGETリクエストを送る
        response = self.client.get(url)

        # ステータスコードが200であることを確認
        self.assertEqual(response.status_code, 200)
```

---

## setUp について

各テストメソッドが実行される直前に毎回呼ばれる**初期化用メソッド**。

### 💡 内容

- 各テストの直前に毎回実行される。
- 各テスト間でデータが影響し合わないようにするため、テストごとにインスタンスが破棄されて再生成される。
- 複数のテストで同じデータ（ユーザー・URLなど）を使い回したい場合、`setUp` でまとめてセットしておくとDRYになる。

### ✒️ 基本的な書き方

```python
class AccountsTest(TestCase):
    def setUp(self):
        # テスト用のユーザーを作成
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        # 複数テストで使うURLもここで作っておく
        self.url = reverse("test_open")

    def test_test_open_not_login(self):
        # setUp で作った self.url を使う
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_test_open_login(self):
        # こちらのテストでも setUp で作った self.url を再利用できる
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
```

---

## self.client について

`TestCase` が用意してくれている**テスト用ブラウザ**みたいなもの。

### 💡 内容

- `self.client.get(url)` でGETリクエストを送れる。
- 戻り値は `HttpResponse` オブジェクト（`response`）で、ステータスコードやテンプレート、contextなどを後から検証できる。
- `self.client.login(...)` でログイン済み状態を作れる（通常のビューで使う `authenticate` + `login` のテスト用ショートカット）。

### ✒️ 基本的な書き方

```python
# GETリクエスト
response = self.client.get(self.url)

# ログイン状態を作る
self.client.login(username="testuser", password="testpassword")
```

### 💡 通常の `authenticate` + `login` との違い

| 場面                               | 使うもの                                        |
| ---------------------------------- | ----------------------------------------------- |
| 実際のビューでログイン処理を書く   | `authenticate()` + `login(request, user)`       |
| テストでログイン済み状態を作りたい | `self.client.login(username=..., password=...)` |

`login(request, user)` は `request` オブジェクトを必要とするが、テスト中にはまだ `request` がないため、それを内部でうまくやってくれる `self.client.login()` を使う。

---

## response の属性

レスポンスオブジェクトには色々な情報が詰まっており、テストではこれらを取り出して検証する。

### 💡 よく使う属性一覧

| 属性                   | 中身                                           | 用途                                     |
| ---------------------- | ---------------------------------------------- | ---------------------------------------- |
| `response.status_code` | HTTPステータスコード（200、302、404、500など） | 正常表示・リダイレクト・エラーの判定     |
| `response.context`     | テンプレートに渡された変数たち（辞書）         | ビューが正しいデータを渡しているかの確認 |

### ✒️ 基本的な書き方

```python
response = self.client.get(self.url)

# ステータスコード
response.status_code              # → 200, 302, 404 など

# テンプレートに渡された変数
response.context["page_title"]    # → "勉強場1"
response.context["input_form"]    # → TestFormのインスタンス
```

---

## assert系メソッドについて

`TestCase` クラス（厳密には `unittest.TestCase`）が用意してくれている、結果を検証するためのメソッド群。

### 💡 内容

- **成功時は何も返さない（`None`）**。次の行へ進むだけ。
- **失敗時は `AssertionError` を出してテストを止める**。テストランナーが「FAIL」として集計してくれる。
- Python組み込みの `assert` 文でも近いことはできるが、テストでは専用メソッドの方が便利（失敗時のメッセージが親切、`python -O` で消えない、テストランナーが集計できる、など）。
- Django独自というよりは、Python標準の `unittest` の機能をDjangoが拡張して使っている。

### 💡 よく使うメソッド一覧

| メソッド名                           | 役割                                  |
| ------------------------------------ | ------------------------------------- |
| `assertEqual(a, b)`                  | `a == b` を確認                       |
| `assertIsInstance(obj, cls)`         | `obj` が `cls` のインスタンスかを確認 |
| `assertTemplateUsed(response, name)` | 指定したテンプレートが使われたか確認  |

### ✒️ 基本的な書き方

```python
# ステータスコードの確認
self.assertEqual(response.status_code, 200)

# テンプレートの確認
self.assertTemplateUsed(response, "test.html")

# contextの中身の確認
self.assertEqual(response.context["page_title"], "勉強場1")

# 渡されたフォームが正しい型かの確認
self.assertIsInstance(response.context["input_form"], TestForm)
```

---

## assertTemplateUsed について

レンダリングに使われたテンプレートが、想定したものと一致しているかを確認するメソッド。

### 💡 内容

- ステータスコードが200でも、**意図しないテンプレートが使われている可能性**があるため、確認するために使う。
- 役に立つ場面の例(多分):
  - テンプレート名を間違えて編集してしまった

### ✒️ 基本的な書き方

```python
# 使われたテンプレートを確認
self.assertTemplateUsed(response, "test.html")
```

---

## response.context の確認

ビューがテンプレートに渡したデータ（context）の中身が正しいかを確認する。

### 💡 内容

- `response.context["キー名"]` で、ビューで `render` の第3引数に渡した辞書のキーから値を取り出せる。
- 「正しいテンプレートが使われた」だけでなく、「正しいデータが渡されている」までを検証することで、ビューの挙動をより細かく担保できる。

### ✒️ 基本的な書き方

```python
# ビュー側で渡された値の確認
self.assertEqual(response.context["page_title"], "勉強場1")

# 渡されたフォームが正しい型か確認
self.assertIsInstance(response.context["input_form"], TestForm)
self.assertIsInstance(response.context["select_form"], TestSelect)
self.assertIsInstance(response.context["book_form"], BookForm)
```

### 💡 context の補足

「context」はDjango用語というよりプログラミング全般で使われる言葉で、ざっくり**「処理に必要な周辺情報のセット」**という意味。Djangoのテンプレートcontextも「テンプレートを描画する文脈として、これらの変数が使えるよ」というデータのかたまりを指す。

---

## テストの実行方法

`manage.py test` の引数で実行範囲を絞り込める。

### 💡 内容

- `manage.py` がある階層で実行する。
- ドット区切りで「アプリ名.テストファイル.クラス名.メソッド名」を指定すると、その範囲に絞ってテストを実行できる。
- `-v 2` を付けるとどのテストが走ったかが詳しく表示される。

### ✒️ 基本的な書き方

```bash
# アプリ全体のテストを実行
python manage.py test accounts

# tests.py の中の全テストを実行
python manage.py test accounts.tests

# クラス単位で実行
python manage.py test accounts.tests.AccountsTest

# 1つのメソッドだけ実行
python manage.py test accounts.tests.AccountsTest.test_test_open_not_login

```

---

## テストコード全体の例

```python
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .forms import *

User = get_user_model()


class BookTestCase(TestCase):
    def test_book_list_page_returns_200(self):
        url = reverse("book_list_open")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class AccountsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.url = reverse("test_open")

    def test_test_open_not_login(self):
        """1. 未ログイン状態のテスト"""
        response = self.client.get(self.url)
        # @login_required によって弾かれ、リダイレクト（302）されることを確認
        self.assertEqual(response.status_code, 302)

    def test_test_open_login(self):
        """2. ログイン状態のテスト"""
        # テストユーザーでログイン
        self.client.login(username="testuser", password="testpassword")

        response = self.client.get(self.url)

        # ステータスコードの確認
        self.assertEqual(response.status_code, 200)

        # 使われたテンプレートの確認
        self.assertTemplateUsed(response, "test.html")

        # テンプレートに渡されたデータ（context）の中身の確認
        self.assertEqual(response.context["page_title"], "勉強場1")

        # 渡されたフォームが正しい型のインスタンスか確認
        self.assertIsInstance(response.context["input_form"], TestForm)
        self.assertIsInstance(response.context["select_form"], TestSelect)
        self.assertIsInstance(response.context["book_form"], BookForm)
```

---
