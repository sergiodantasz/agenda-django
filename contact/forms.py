from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from contact import models


class ContactForm(forms.ModelForm):
    picture = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                'accept': 'image/*',
            }
        )
    )

    class Meta:
        model = models.Contact
        fields = (
            'first_name', 'last_name', 'phone', 'email', 'description', 'category', 'picture'
        )


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        required=True,
        min_length=3
    )
    last_name = forms.CharField(
        required=True,
        min_length=3
    )
    email = forms.EmailField(
        required=True,
        min_length=5
    )

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email', 'username', 'password1', 'password2'
        )
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            self.add_error(
                'email',
                ValidationError(
                    'Este e-mail já foi registrado.',
                    code='invalid'
                )
            )
        return email
