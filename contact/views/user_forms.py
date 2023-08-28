from django.contrib import messages, auth
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render

from contact.forms import RegisterForm


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário registrado com sucesso.')
            return redirect('contact:login')
    else:
        form = RegisterForm()
    return render(
        request,
        'contact/register.html',
        {
            'form': form,
        }
    )


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            messages.success(request, 'Login efetuado com sucesso.')
            return redirect('contact:index')
        messages.error(request, 'Usuário ou senha incorretos.')
    else:
        form = AuthenticationForm(request)
    return render(
        request,
        'contact/login.html',
        {
            'form': form,
        }
    )


def logout_view(request):
    auth.logout(request)
    return redirect('contact:login')
