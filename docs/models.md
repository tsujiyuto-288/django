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

| オプション        | 意味                            |
| ----------------- | ------------------------------- |
| max_length        | 最大文字数（CharFieldでは必須） |
| null=True         | DBにNULLを許可する              |
| blank=True        | フォームで空欄を許可する        |
| default           | デフォルト値を設定する          |
| unique=True       | 重複を禁止する                  |
| auto_now=True     | 保存のたびに現在日時をセット    |
| auto_now_add=True | 作成時のみ現在日時をセット      |

### 🌌空欄を許可したい場合
**🚨Djangoのフォームバリデーションを使用する場合はblank=Trueの設定が必要**

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
