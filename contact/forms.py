from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from contact.models import Contact, Profile


class PictureInput(forms.ClearableFileInput):
    template_name = "contact/widgets/picture_input.html"


class StyledFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            if isinstance(
                widget,
                (
                    forms.CheckboxInput,
                    forms.RadioSelect,
                    forms.HiddenInput,
                    forms.ClearableFileInput,
                ),
            ):
                continue
            classes = widget.attrs.get("class", "")
            if "form-control" not in classes.split():
                widget.attrs["class"] = f"form-control {classes}".rstrip()


class UniqueEmailMixin:
    error_message = "Este e-mail já está cadastrado."

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email:
            return email
        queryset = User.objects.filter(email__iexact=email)
        if self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise forms.ValidationError(self.error_message, code="invalid")
        return email


class ContactForm(StyledFormMixin, forms.ModelForm):
    picture = forms.ImageField(
        label="Foto",
        required=False,
        widget=PictureInput(attrs={"accept": "image/*"}),
    )

    class Meta:
        model = Contact
        fields = (
            "first_name",
            "last_name",
            "phone",
            "email",
            "description",
            "category",
            "picture",
        )
        widgets = {  # noqa: RUF012
            "first_name": forms.TextInput(attrs={"placeholder": "Ex.: Maria"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Ex.: Silva"}),
            "phone": forms.TextInput(
                attrs={"placeholder": "Ex.: (11) 99999-9999", "autocomplete": "tel"}
            ),
            "email": forms.EmailInput(
                attrs={"placeholder": "Ex.: maria@email.com", "autocomplete": "email"}
            ),
            "description": forms.Textarea(attrs={"rows": 4}),
            "category": forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].empty_label = "Sem categoria"


class RegisterForm(StyledFormMixin, UserCreationForm, UniqueEmailMixin):
    first_name = forms.CharField(max_length=30, required=True, label="Nome")
    last_name = forms.CharField(max_length=150, required=True, label="Sobrenome")
    email = forms.EmailField(required=True, label="E-mail")
    picture = forms.ImageField(
        label="Foto de perfil",
        required=False,
        widget=PictureInput(attrs={"accept": "image/*"}),
    )

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "username",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Usuário"
        self.fields["username"].widget.attrs["autocomplete"] = "username"
        self.fields[
            "username"
        ].help_text = (
            "Obrigatório. 150 caracteres ou menos. Letras, números e @/./+/-/_."
        )
        self.fields["password1"].label = "Senha"
        self.fields["password1"].widget.attrs["autocomplete"] = "new-password"
        self.fields["password2"].label = "Confirmação de senha"
        self.fields["password2"].widget.attrs["autocomplete"] = "new-password"
        self.fields[
            "password2"
        ].help_text = "Informe a mesma senha anterior, para verificação."

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            picture = self.cleaned_data.get("picture")
            if picture:
                profile, _ = Profile.objects.get_or_create(user=user)
                profile.picture = picture
                profile.save()
        return user


class RegisterUpdateForm(StyledFormMixin, UniqueEmailMixin, forms.ModelForm):
    first_name = forms.CharField(
        min_length=2,
        max_length=30,
        required=True,
        label="Nome",
    )
    last_name = forms.CharField(
        min_length=2,
        max_length=150,
        required=True,
        label="Sobrenome",
    )
    password1 = forms.CharField(
        label="Senha",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
        required=False,
    )
    password2 = forms.CharField(
        label="Confirmação de senha",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text="Informe a mesma senha anterior, para verificação.",
        required=False,
    )
    picture = forms.ImageField(
        label="Foto de perfil",
        required=False,
        widget=PictureInput(attrs={"accept": "image/*"}),
    )

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "username",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Usuário"
        self.fields["username"].widget.attrs["autocomplete"] = "username"
        self.fields["email"].widget.attrs["autocomplete"] = "email"
        self.fields[
            "username"
        ].help_text = (
            "Obrigatório. 150 caracteres ou menos. Letras, números e @/./+/-/_."
        )
        profile = Profile.objects.filter(user=self.instance).first()
        if profile and profile.picture:
            self.initial["picture"] = profile.picture

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if (password1 or password2) and password1 != password2:
            self.add_error(
                "password2",
                "A confirmação de senha deve ser idêntica à senha.",
            )
        return cleaned_data

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if password1:
            password_validation.validate_password(password1, self.instance)
        return password1

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password1")
        if password:
            user.set_password(password)
        if commit:
            user.save()
        picture = self.cleaned_data.get("picture")
        profile, _ = Profile.objects.get_or_create(user=user)
        if "picture-clear" in self.data:
            if profile.picture:
                profile.picture.delete(save=False)
            profile.picture = ""
        elif picture:
            profile.picture = picture
        profile.save()
        return user


class LoginForm(StyledFormMixin, AuthenticationForm):
    username = forms.CharField(
        label="Usuário",
        widget=forms.TextInput(attrs={"autocomplete": "username"}),
    )
    password = forms.CharField(
        label="Senha",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )
