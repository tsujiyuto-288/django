# Djangoの主要メソッド

## reverse() とは

`urls.py` で定義した **「URLの名前（nameパラメータ）」** から、対応する **「実際のURL文字列（パス）」** を逆算（逆引き）して取得するための関数。

### 💡 概要

- `django.urls` モジュールからインポートして使用する（`from django.urls import reverse`）。
- 第1引数に `urls.py` で指定した `name` を渡すと、実際のURL文字列（例：`/book_list/`）が返される。
