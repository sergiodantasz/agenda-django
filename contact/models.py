from django.db import models
from django.utils import timezone


class Contact(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=254, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    description = models.TextField(blank=True)
    show = models.BooleanField(default=True)
    picture = models.ImageField(upload_to=r'pictures/%Y/%m/%d/', blank=True)

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}' if self.last_name else self.first_name