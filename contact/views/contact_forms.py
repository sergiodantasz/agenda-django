from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from contact.forms import ContactForm
from contact import models


@login_required(login_url='contact:login')
def create(request):
    form_action = reverse('contact:create')
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)
    else:
        form = ContactForm()
    context = {
        'site_title': 'Create - ',
        'form': form,
        'form_action': form_action
    }
    if form.is_valid():
        contact = form.save(commit=False)
        contact.owner = request.user
        contact.save()
        return redirect('contact:update', contact_id=contact.pk)
    return render(
        request,
        'contact/create.html',
        context=context
    )


@login_required(login_url='contact:login')
def update(request, contact_id):
    contact = get_object_or_404(
        models.Contact,
        pk=contact_id,
        show=True,
        owner=request.user
    )
    form_action = reverse('contact:update', args=(contact_id,))
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES, instance=contact)
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


@login_required(login_url='contact:login')
def delete(request, contact_id):
    contact = get_object_or_404(
        models.Contact,
        pk=contact_id,
        show=True,
        owner=request.user
    )
    confirmation = request.POST.get('confirmation', 'no')
    if confirmation == 'yes':
        contact.delete()
        return redirect('contact:index')
    return render(
        request,
        'contact/contact.html',
        {
            'contact': contact,
            'confirmation': confirmation
        }
    )
