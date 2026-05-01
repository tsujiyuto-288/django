from django import forms
from accounts.models import Book


class TestForm(forms.Form):
    book_title = forms.CharField(
        max_length=10,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3 book_title",
                "placeholder": "タイトル(10文字まで)",
            }
        ),
    )


class TestSelect(forms.Form):
    TEST_CHOICES = (
        ("order", "発注待ち"),
        ("waiting", "陳列待ち"),
        ("completion", "陳列済み"),
    )
    book_status = forms.ChoiceField(
        choices=TEST_CHOICES,
        widget=forms.Select(
            attrs={
                "class": "form-select mb-3 book_status",
            }
        ),
    )


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control mb-3 book_title",
                    "placeholder": "タイトル(10文字まで)",
                }
            ),
        }

    def clean_title(self):
        title = self.cleaned_data["title"]
        title = title.strip()  # 毎回走らせたい処理を書くことができる
        if "テスト" in title:  # バリデーションを独自に追加もできる
            raise forms.ValidationError("タイトルに『テスト』は使用できません")
        return title
