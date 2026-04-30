# HTTPレスポンスについて

## HTTPレスポンス (HttpResponse) とは

Djangoのビュー関数がブラウザ（やJavaScript）に返す**最終的な結果の「箱」**のこと。
ビューは**必ず何かしらのHTTPレスポンスを返さなければならない**という絶対のルールがある。

### 💡 なぜ色々な種類があるのか？

最も基礎となる `HttpResponse` は、「ただの文字列」を返すだけのシンプルな箱であるため、非常に扱いづらい。
例えば、辞書（dict）を返してもブラウザはただの文字列として表示してしまうし、複雑なHTMLをすべて文字列で手書きするのは不可能に近い。
そのため、用途に合わせて「箱の中身を自動で綺麗に整えてくれる便利な包み紙（ラッパー）」として、`render` や `JsonResponse` などが用意されている。

---

## よく使われるレスポンス一覧

### 💡 概要

全体の95%以上は `render`, `redirect`, `JsonResponse` の3つで完結する。

| クラス / 関数名 | 返すもの | 用途・特徴 |
| --- | --- | --- |
| `render()` | HTML文字列を詰めたレスポンス | テンプレート（HTML）と辞書（データ）を合成し、キレイなHTML画面を生成して返す。**通常の画面表示用。** |
| `redirect()` | 「別URLへ移動しろ」という指示 | データの保存処理などの後、別のページに強制的に遷移させる時に使う。二重送信の防止（PRGパターン）などに必須。 |
| `JsonResponse()` | JSON形式に変換したレスポンス | 辞書（dict）を自動でJSONの文字列に変換して返す。**Ajax（非同期通信）でJavaScriptにデータを渡す専用。** |
| `HttpResponse()` | ただの文字列やバイトデータ | 最も原始的なレスポンス。全てのレスポンスの親玉だが、単体で使われることは少ない。 |
| `FileResponse()` | ファイルのストリームデータ | PDFやCSVなどの「ファイルのダウンロード」や「ブラウザ上でのファイル表示」を行う時に使う。 |

---

### ✒️ 基本的な書き方

```python
# --- 1. render() ---
# 第1引数: request（必須）
# 第2引数: 表示させるHTMLのファイル名
# 第3引数: テンプレートタグ（{{ }}）に当てはめるためのデータ（辞書）
return render(request, "test.html", {"page_title": "テストページ"})


# --- 2. redirect() ---
# urls.py で定義した name（推奨）、または直接URLを指定する
return redirect("test_open")


# --- 3. JsonResponse() ---
# Pythonの辞書を渡すと、JSが読めるJSONに自動変換して返してくれる
return JsonResponse({"status": "success", "message": "登録完了"})


# --- 4. HttpResponse() ---
# ただの文字列を返すだけ（実務で直接使うことは稀）
from django.http import HttpResponse

return HttpResponse("<h1>ただの文字列です</h1>")


# --- 5. FileResponse() ---
# ファイルを開いて渡すことで、ダウンロードさせることができる
from django.http import FileResponse

file = open('sample.pdf', 'rb')
return FileResponse(file, as_attachment=True) # as_attachment=Trueで強制ダウンロード
```

---

## ステータスコード指定用のレスポンス（エラー通知系）

### 💡 概要

「このリクエストはおかしい」「権限がない」「ページがない」といったエラーを、ブラウザに対して**明示的なHTTPステータスコード（400番台など）と共に伝える**ために使うレスポンス。

| クラス名 | ステータス | 用途・意味 |
| --- | --- | --- |
| `HttpResponseBadRequest` | 400 | 不正なリクエスト（必須データがない、形式がおかしい等）の時に使う。 |
| `HttpResponseForbidden` | 403 | 権限エラー（ログインはしているが、その機能を使う権限がない等）の時に使う。 |
| `HttpResponseNotFound` | 404 | 指定されたデータやURLが存在しない時に使う。 |
| `HttpResponseNotAllowed` | 405 | 許可されていないメソッド（GET専用のURLにPOSTでアクセスされた等）の時に使う。 |

### ✒️ 基本的な書き方

```python
from django.http import HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotAllowed

# 400 Bad Request
return HttpResponseBadRequest("必要なデータが足りません。")

# 403 Forbidden
return HttpResponseForbidden("管理者権限が必要です。")

# 405 Method Not Allowed
# リスト形式で「許可されているメソッド」を引数に渡すルールがある
return HttpResponseNotAllowed(["POST"])
```
