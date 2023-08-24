from django.shortcuts import redirect, render

from contact.forms import ContactForm


def create(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
    else:
        form = ContactForm()
    if form.is_valid():
        form.save()
        redirect('contact:create')
    return render(
        request,
        'contact/create.html',
        context={
            'site_title': 'Create - ',
            'form': form
        }
    )
