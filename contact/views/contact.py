from django.shortcuts import render

from contact.models import Contact


def index(request):
    contacts = Contact.objects.all()
    return render(
        request,
        'contact/index.html',
        context={
            'contacts': contacts,
        }
    )
