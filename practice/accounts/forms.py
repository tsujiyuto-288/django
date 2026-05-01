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
        fields = ["title", "status"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control mb-3 book_title",
                    "placeholder": "タイトル(10文字まで)",
                }
            ),
            "status": forms.Select(attrs={"class": "form-select mb-3 book_status"}),
        }
