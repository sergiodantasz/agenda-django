from django.shortcuts import render

from contact.models import Contact


def index(request):
    contacts = Contact.objects.filter(show=True).order_by('-id')
    contacts = contacts[:10]  # DEBUG
    return render(
        request,
        'contact/index.html',
        context={
            'contacts': contacts,
        }
    )
