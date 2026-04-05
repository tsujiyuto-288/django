# モデルについて

## モデル作成方法

- `models.Model` を継承してテーブルを定義する

### ✒️書き方

```python
class モデル名(models.Model):
```

## モデルの設定

- モデルクラスの中に`class Meta:` を書くことでモデルの様々な設定ができる。

### ✒️書き方

```python
class User(model.Model):
    class Meta:
        db_table = "user"
        verbose_name = "本データ"
        などなど....
```

### 💡設定項目

| 設定         | 意味                                                             |
| ------------ | ---------------------------------------------------------------- |
| db_table     | データベースのテーブル名　デフォルトではアプリ名\_モデル名になる |
| verbose_name | 管理画面での表示名                                               |

## フィールドの作成(設定)

- モデルクラスの中に`フィールド名 = models.フィールドクラス(オプション)`と書くことでフィールドを作成できる

### 💡フィールドクラス

| フィールド    | 保存できる値      | 備考                             |
| ------------- | ----------------- | -------------------------------- |
| CharField     | str(設定する)     | `max_length` が必須              |
| TextField     | str               | 文字数制限なし、改行も保存される |
| BooleanField  | bool              |                                  |
| IntegerField  | int               |                                  |
| DateField     | datetime.date     | 例: 2026-04-02                   |
| DateTimeField | datetime.datetime | 例: 2026-04-02 14:30:00          |
| EmailField    | str(254)          | バリデーション付きのCharField    |
| FileField     | str(100)          | メディアファイルのパスを保存     |

### 💡よく使うフィールドオプション

| オプション        | 意味                                                                                        |
| ----------------- | ------------------------------------------------------------------------------------------- |
| verbosename       | フィールド名を設定する                                                                      |
| primary_key       | Trueにすることで設定したフィールドが主キーになる                                            |
| on_delete         | 関連するモデルオブジェクトが削除された際の挙動を設定(OneToOneFieldとForeginKeyでは設定必須) |
| choices           | 登録できる値を制限する                                                                      |
| max_length        | 最大文字数（CharFieldでは必須）                                                             |
| null=True         | DBにNULLを許可する                                                                          |
| blank=True        | フォームで空欄を許可する                                                                    |
| default           | デフォルト値を設定する                                                                      |
| unique=True       | 重複を禁止する                                                                              |
| auto_now=True     | 保存のたびに現在日時をセット                                                                |
| auto_now_add=True | 作成時のみ現在日時をセット                                                                  |

---

#### ■ choicesについて

選択肢の中から保存する値を選びたい。
選択肢以外の値を保存したくない。
というときに使用する。
選択肢は`("dbに保存される値","ラベル名")`と設定する

ただし、choicesはデータベースレベルの制約ではない点に注意。(選択肢以外のものも保存できる)

**choicesの主な役割：**

- コードの可読性向上（このフィールドにはどんな値が入る想定なのかが明確になる）
- Django Adminなどの管理サイトでプルダウン表示になり、手動でのデータ登録時に操作しやすくなる

**注意点：**

- `model.save()` や `Model.objects.create()` などフォームを経由せず直接保存する場合、choices以外の値でもエラーにならずそのまま保存される

```python
#基本的な書き方
TEST_CHOICES = [
    ("yes","合格"),
    ("no","失敗"),
    ("hold","保留"),
]
test = models.CharField(
    max_length=10,
    choices=TEST_CHOICES,
)
```


### 🌌空欄を許可したい場合

#### 文字列の場合

nullと空文字("")の2パターンが存在するとややこしくなるのでデフォルトを空文字にしつつnullをFalseにする。

```python
default="",
null=False,#指定しなくてもnullはFalseなので実際は書かなくていい
```

#### 数字系(int,date)の場合

intやdateには""(空文字)という概念がないので未入力を表すにはNullを使うしかないが
空欄(null)はデフォルトだと弾く設定になっているので許可するようにする必要がある。

```python
null=True,
default=None,#指定しなくてもdefaultはNoneなので実際は書かなくていい
```

**🚨Djangoのフォームバリデーションを使用する場合はblank=Trueの設定が必要**

---

### ⭐️1対1のリレーションについて

関係性が1対1で表せるものに対して使用する。

**例：**

- ユーザー情報 ↔ シークレット情報（パスワード、クレカ番号など）
- 本 ↔ 本の在庫数
- システム利用者 ↔ お気に入りリスト

**書き方：**

参照元に `OneToOneField` を定義し、第一引数に参照先のモデル名を指定する。

```python
class Book_Stock(models.Model):
    book = models.OneToOneField(
        "Book",
        on_delete=models.CASCADE,
    )
```

**参照の仕方：**

参照している側からの場合：

- `フィールド名_id` → 参照先の主キー(pk)が取れる
- `フィールド名` → 参照先のオブジェクトが取れる

```python
#例
stock = Book_Stock.objects.get(id=1)
stock.book_id   # Bookの主キー
stock.book      # Bookオブジェクト

```

逆参照（参照されている側からの場合）：

- `参照元モデル名の小文字` → 参照元のオブジェクトが取れる

```python
#例
book = Book.objects.get(id=1)
book.book_stock　#Book_Stockオブジェクト
```

---

### 🌠1対多のリレーションについて

関係性が1対多で表せるものに対して使用する。

**例：**

- ユーザー情報 ↔ 所属企業
- 本 ↔ 出版社
- SNSアカウント ↔ 投稿

**書き方：**

多側に `ForeignKey` を定義し、第一引数に参照先(1側)のモデル名を指定する。

```python
class Book(models.Model):
    company = models.ForeignKey(
        "Company",
        verbose_name="出版社",
        on_delete=models.CASCADE
    )
```

**参照の仕方：**

参照している側(多側)からの場合：

- `フィールド名_id` → 参照先(1側)の主キー(pk)が取れる
- `フィールド名` → 参照先(1側)のオブジェクトが取れる

```python
#例
book = Book.objects.get(id=1)
book.company_id   # companyの主キー
book.company      # companyオブジェクト

```

逆参照（参照されている(1側)側からの場合）：

- `参照元モデル名の小文字_set` → 参照元(多側)の**モデルマネージャー**

```python
#例
company = Company.objects.get(id=1)
company.book_set # このbook_setはモデルマネージャー
```

---

### 🌌多対多のリレーションについて

関係性が多対多で表せるものに対して使用する。

**例：**

- 本 ↔ 読者
- 投稿 ↔ 閲覧者

**書き方：**

片方に `ManyToManyField` を定義し、第一引数に参照先のモデル名を指定する。

```python
class Book(models.Model):
    author = models.ManyToManyField(
        "Author", 
        verbose_name="著者",
    )
```

**参照の仕方：**

参照している側からの場合：

- `フィールド名` → 参照先の**モデルマネージャー**

```python
#例
book = Book.objects.get(id=1)
book.author   # このauthorはモデルマネージャー

```

逆参照（参照されている側からの場合）：

- `参照元モデル名の小文字_set` → 参照先の**モデルマネージャー**

```python
#例
author = Author.objects.get(id=1)
author.book_set # このbook_setはモデルマネージャー
```

---

#### ■ on_delete について

**参照先が削除されたとき、参照元をどうするか**を決める設定。

| 設定        | 参照先が削除されたとき        |
| ----------- | ----------------------------- |
| CASCADE     | 参照元も一緒に削除される      |
| PROTECT     | 削除をブロックする            |
| SET_NULL    | NULLになる（null=Trueが必要） |
| SET_DEFAULT | default値になる               |

**💡外部キーをどちらに持たせるか**

外部キー（`OneToOneField` / `ForeignKey`）は**依存する側（従属する側）に持たせる**。

> 「AがなければBは存在しない」→ **B側にAへの参照を持たせる**

こうすることで `on_delete=CASCADE` が「Aを消したらBも消える」という自然な意味になる。

**逆にしてしまうと「Bを消したらAも消える」となり、意図しない削除が発生する。**

---
