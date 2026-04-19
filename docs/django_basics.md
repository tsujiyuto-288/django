# Djangoの基本知識まとめ

## render() について

「画面（HTML）」と「データ」をセットにしてブラウザに返すための、最も一般的なショートカット関数。

### 💡 概要

- 内部でHTMLテンプレートの読み込みとデータの埋め込みを行い、最終的に `HttpResponse` として返す一連の処理をまとめてやってくれる。
- 特殊な要件がない限り、画面を表示する際はこの `render()` を使うのが基本。
- 第3引数に渡すデータは、必ず **辞書型** でなければならないというルールがある。（例：`{"book": book}`）

### ✒️ 基本的な書き方

```python
from django.shortcuts import render

# 基本的な使い方：第3引数で辞書型にしてデータを渡す
def my_view(request):
    book = Book.objects.get(id=1)
    return render(request, "test2.html", {"book": book})
```

---

## JsonResponse について

Pythonのデータ（辞書型やリスト型など）を、システム間でやり取りしやすい **JSON形式** に変換してブラウザへ返すクラス。

### 💡 概要

- 画面の遷移（ページ移動）は行わず、バックグラウンド（AJAX非同期通信など）で「データだけ」をやり取りしたい場合に使用する。
- デフォルトでは辞書型（`dict`）を受け取るようになっている。リスト型などを渡したい場合は `safe=False` という引数を追加する必要がある。

### ✒️ 基本的な書き方

```python
from django.http import JsonResponse

# 基本的な使い方：辞書型をそのまま渡す
def my_api_view(request):
    data = {
        "status": "success",
        "message": "登録が完了しました"
    }
    # 辞書型をJSONにして返す（画面遷移はしない）
    return JsonResponse(data)

# リスト型など辞書以外を返す場合
def list_api_view(request):
    titles = ["銀河鉄道の夜", "人間失格"]
    # safe=False をつける必要がある
    return JsonResponse(titles, safe=False)
```

---

## TemplateResponse について

指定されたHTMLファイルにデータを埋め込んでWebページとして返すクラス。目標としている結果は `render()` と同じ。

### 💡 概要

- `render()` との違いは、「レスポンスがブラウザに返される直前までHTMLの確定（レンダリング）を遅らせることができる」点にある。
- ビューの処理が終わったあとに、ミドルウェアなどで「後から変数やテンプレートを書き換えたい」といった、高度で特殊な処理が必要な場合に使われる。
- そのため、通常の画面表示の用途であれば `render()` を使用すればよく、`TemplateResponse` は基本的に不要。

### ✒️ 基本的な書き方

```python
from django.template.response import TemplateResponse

# 基本的な書き方（引数の構成などはrenderと同じ）
def my_view(request):
    book = Book.objects.get(id=1)
    return TemplateResponse(request, "test2.html", {"book": book})
```

---

## 現在の日付・時刻の取得について

Djangoプロジェクト内で現在の日付や時刻を取得する際は、Djangoが用意している`timezone` を使用することが推奨されている。

### 💡 概要

- Python標準の `datetime` モジュールを使用するのではなく、Djangoの `timezone` モジュールを使用することで、タイムゾーンを考慮した正確な日時を安全に扱うことができる。
- 日付だけが必要な場合は `localdate()`、時刻も含めた日時が必要な場合は `localtime()` などが用意されている。

### ✒️ 基本的な書き方

```python
from django.utils import timezone

# 今日の日付を取得する場合
today = timezone.localdate()

# 現在の日時（日付＋時刻）を取得する場合
now = timezone.localtime()
```

---
