from django.contrib import messages
from django.shortcuts import redirect, render

from contact.forms import RegisterForm


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário registrado com sucesso.')
            return redirect('contact:index')
    else:
        form = RegisterForm()
    return render(
        request,
        'contact/register.html',
        {
            'form': form,
        }
    )
