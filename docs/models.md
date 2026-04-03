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

#### choicesについて

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
