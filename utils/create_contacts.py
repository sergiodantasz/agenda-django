from os import environ
from pathlib import Path
from random import choice
from sys import path

from django import setup
from django.conf import settings

from faker import Faker

DJANGO_BASE_DIR = Path(__file__).parent.parent

NUMBER_OF_OBJECTS = 1000

path.append(str(DJANGO_BASE_DIR))
environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'
settings.USE_TZ = False

setup()

from contact.models import Category, Contact

Contact.objects.all().delete()
Category.objects.all().delete()

fake = Faker('pt_BR')
categories = ('Amigos', 'Família', 'Conhecidos')

django_categories = [
    Category(name=name) for name in categories
]

for category in django_categories:
    category.save()
  
django_contacts = []

for _ in range(NUMBER_OF_OBJECTS):
    profile = fake.profile()
    email = profile.get('mail')
    first_name, last_name = profile.get('name').split(' ', 1)
    phone = fake.phone_number()
    created_date = fake.date_this_year()
    description = fake.text(max_nb_chars=100)
    category = choice(django_categories)

    django_contacts.append(
        Contact(
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            email=email,
            created_date=created_date,
            description=description,
            category=category
        )
    )

if len(django_contacts) > 0:
    Contact.objects.bulk_create(django_contacts)
