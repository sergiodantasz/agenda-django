from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from contact.forms import ContactForm
from contact import models


def create(request):
    form_action = reverse('contact:create')
    if request.method == 'POST':
        form = ContactForm(request.POST)
    else:
        form = ContactForm()
    context = {
        'site_title': 'Create - ',
        'form': form,
        'form_action': form_action
    }
    if form.is_valid():
        contact = form.save()
        return redirect('contact:update', contact_id=contact.pk)
    return render(
        request,
        'contact/create.html',
        context=context
    )


def update(request, contact_id):
    contact = get_object_or_404(
        models.Contact,
        pk=contact_id,
        show=True
    )
    form_action = reverse('contact:update', args=(contact_id,))
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
    else:
        form = ContactForm(instance=contact)
    context = {
        'site_title': 'Create - ',
        'form': form,
        'form_action': form_action
    }
    if form.is_valid():
        contact = form.save()
        return redirect('contact:update', contact_id=contact.pk)
    return render(
        request,
        'contact/create.html',
        context=context
    )
