from django import forms
from django.core.exceptions import ValidationError

from contact import models


class ContactForm(forms.ModelForm):
    class Meta:
        model = models.Contact
        fields = (
            'first_name', 'last_name', 'phone', 'email', 'description', 'category'
        )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def clean(self):
        cleaned_data = self.cleaned_data
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        if last_name == first_name:
            self.add_error(
                'last_name',
                ValidationError(
                    'O último nome não pode ser igual ao primeiro nome.',
                    code='invalid'
                )
            )
        return super().clean()
