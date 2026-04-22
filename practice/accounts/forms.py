from django import forms


class TestForm(forms.Form):
    book_title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3 book_title",
                "placeholder": "タイトル",
            }
        )
    )
