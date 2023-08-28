from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render

from contact.forms import RegisterForm, RegisterUpdateForm


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


@login_required(login_url='contact:login')
def logout_view(request):
    auth.logout(request)
    return redirect('contact:login')


@login_required(login_url='contact:login')
def user_update(request):
    if request.method == 'POST':
        form = RegisterUpdateForm(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('contact:user_update')
    else:
        form = RegisterUpdateForm(instance=request.user)
    return render(
        request,
        'contact/user_update.html',
        {
            'form': form
        }
    )
