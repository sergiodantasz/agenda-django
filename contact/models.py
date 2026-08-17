import re

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

PHONE_RE = re.compile(r"^\+?[0-9\s().-]{8,20}$")


def validate_phone(value: str) -> None:
    if not PHONE_RE.fullmatch(value):
        raise ValidationError(
            "Informe um telefone válido (somente números, espaços e ().- ).",
            code="invalid",
        )


class Category(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name="categoria",
    )

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name


class ContactQuerySet(models.QuerySet):
    def visible(self, user=None) -> ContactQuerySet:
        if not (user and user.is_authenticated):
            return self.none()
        return self.filter(owner=user, show=True)

    def search(self, term: str) -> ContactQuerySet:
        return self.filter(
            models.Q(first_name__icontains=term)
            | models.Q(last_name__icontains=term)
            | models.Q(phone__icontains=term)
            | models.Q(email__icontains=term),
        )


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="usuário",
    )
    picture = models.ImageField(
        upload_to="profiles/%Y/%m/%d/",
        blank=True,
        verbose_name="foto de perfil",
    )

    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfis"

    def __str__(self) -> str:
        return f"Perfil de {self.user.get_full_name() or self.user.username}"


class Contact(models.Model):
    first_name = models.CharField(
        max_length=50,
        verbose_name="nome",
    )
    last_name = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="sobrenome",
    )
    phone = models.CharField(
        max_length=25,
        validators=[validate_phone],
        verbose_name="telefone",
    )
    email = models.EmailField(
        max_length=254,
        blank=True,
        verbose_name="e-mail",
    )
    created_date = models.DateTimeField(
        default=timezone.now,
        verbose_name="criado em",
    )
    description = models.TextField(
        blank=True,
        verbose_name="descrição",
    )
    show = models.BooleanField(
        default=True,
        verbose_name="exibir",
    )
    picture = models.ImageField(
        upload_to="pictures/%Y/%m/%d/",
        blank=True,
        verbose_name="foto",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="contacts",
        verbose_name="categoria",
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="owned_contacts",
        verbose_name="dono",
    )

    objects = ContactQuerySet.as_manager()

    class Meta:
        verbose_name = "Contato"
        verbose_name_plural = "Contatos"
        ordering = ("-id",)

    def get_full_name(self) -> str:
        if self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name

    def __str__(self) -> str:
        return self.get_full_name()
