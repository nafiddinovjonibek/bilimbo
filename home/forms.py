from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import User


class RegisterForm(UserCreationForm):
    ROLE_CHOICES = [
        (User.Role.TARBIYACHI, 'Tarbiyachi'),
        (User.Role.OQUVCHI, "O'quvchi"),
    ]

    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        label='Rol',
        widget=forms.RadioSelect,
        initial=User.Role.OQUVCHI,
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'role', 'password1', 'password2')
        labels = {
            'username': 'Login',
            'first_name': 'Ism',
            'last_name': 'Familiya',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = 'Parol'
        self.fields['password2'].label = 'Parolni tasdiqlang'
        for name, field in self.fields.items():
            if name != 'role':
                field.widget.attrs['class'] = 'input'


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Login'
        self.fields['password'].label = 'Parol'
        for field in self.fields.values():
            field.widget.attrs['class'] = 'input'
