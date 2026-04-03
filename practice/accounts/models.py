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

    quantity = models.OneToOneField(
        "Book_stock",
        verbose_name="在庫(本)",
        on_delete=models.CASCADE,
    )


class Book_stock(models.Model):
    class Meta:
        verbose_name = "在庫"

    quantity = models.IntegerField(
        default=0,
    )
