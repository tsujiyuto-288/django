from django import forms

class LoginForm(forms.Form):    
    username = forms.CharField(
        label="ユーザー名",
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3 username",
                "placeholder": "ユーザー名(アルファベット)",
            }
        ),
    )
    password = forms.CharField(
        label="パスワード",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control mb-3 password",
                "placeholder": "パスワード",
            }
        )
    )

