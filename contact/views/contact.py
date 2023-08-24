from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from contact.models import Contact


def index(request):
    contacts = Contact.objects.filter(show=True).order_by('-id')
    contacts = contacts[:10]  # DEBUG
    return render(
        request,
        'contact/index.html',
        context={
            'contacts': contacts,
            'site_title': 'Contacts - '
        }
    )


def search(request):
    search_value = request.GET.get('q').strip()
    if not search_value:
        return redirect('contact:index')
    contacts = Contact.objects.filter(
        Q(first_name__icontains=search_value) | Q(last_name__icontains=search_value) | Q(phone__icontains=search_value) | Q(email__icontains=search_value),
        show=True,
    ).order_by('-id')
    return render(
        request,
        'contact/index.html',
        context={
            'contacts': contacts,
            'site_title': f'Search ({search_value}) - '
        }
    )


def contact(request, contact_id):
    single_contact = get_object_or_404(
        Contact,
        pk=contact_id,
        show=True
    )
    contact_name = f'{single_contact.first_name} {single_contact.last_name}' if single_contact.last_name else single_contact.first_name
    return render(
        request,
        'contact/contact.html',
        context={
            'contact': single_contact,
            'site_title': f'{contact_name} - '
        }
    )
 