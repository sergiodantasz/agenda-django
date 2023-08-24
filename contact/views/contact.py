from django.shortcuts import get_object_or_404, render

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


def contact(request, contact_id):
    single_contact = get_object_or_404(
        Contact,
        pk=contact_id,
        show=True
    )
    return render(
        request,
        'contact/contact.html',
        context={
            'contact': single_contact,
        }
    )
