from django.db import models


# models.Modelを継承する
class Book(models.Model):
    class Meta:
        db_table = "book"
        verbose_name = "本"

    BOOK_STATUS_CHOICES = (
        ("order", "発注待ち"),
        ("waiting", "陳列待ち"),
        ("completion", "陳列済み"),
    )

    title = models.CharField(
        verbose_name="タイトル",
        max_length=100,
        default="タイトル未入力",
        unique=True,
    )
    # fmt: off
    price = models.IntegerField(
        verbose_name="値段",
        null=True,
        blank=True,
        default=None,
    )
    # fmt: on

    status = models.CharField(
        verbose_name="状態",
        max_length=20,
        choices=BOOK_STATUS_CHOICES,
    )

    # fmt: off
    company = models.ForeignKey(
        "Company", 
        verbose_name="出版社", 
        on_delete=models.CASCADE
    )
    # fmt: on

    # fmt: off
    # 中間テーブルが自動で作成される
    author = models.ManyToManyField(
        "Author", 
        verbose_name="著者",
    )
    # fmt: on


class Book_stock(models.Model):
    class Meta:
        verbose_name = "在庫"

    book = models.OneToOneField(
        "Book",
        verbose_name="本",
        on_delete=models.CASCADE,
    )

    quantity = models.IntegerField(
        default=0,
    )


class Company(models.Model):
    class Meta:
        verbose_name = "出版社"

    name = models.CharField(
        verbose_name="出版社名",
        max_length=50,
    )


class Author(models.Model):
    class Meta:
        verbose_name = "著者"

    name = models.CharField(
        verbose_name="著者名",
        max_length=50,
    )


class E_book(Book):
    class Meta:
        verbose_name = "電子書籍"

    file_size = models.FloatField(
        verbose_name="ファイルサイズ(mb)",
        default=0.0,
    )
    download_url = models.URLField(
        verbose_name="ダウンロードURL",
        blank=True,
        null=True,
    )
