from django.db import models


# models.Modelを継承する
class Book(models.Model):
    class Meta:
        db_table = "book"
        verbose_name = "本データ"

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
        blank=True
        default=None,
    )
    # fmt: on
