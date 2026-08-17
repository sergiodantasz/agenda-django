from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from contact.forms import ContactForm, LoginForm, RegisterForm, RegisterUpdateForm
from contact.models import Contact


class ContactListView(LoginRequiredMixin, ListView):
    model = Contact
    template_name = "contact/contact_list.html"
    context_object_name = "contacts"
    paginate_by = 20

    def get_queryset(self):
        queryset = Contact.objects.visible(self.request.user)
        search_value = self.request.GET.get("q", "").strip()
        if search_value:
            queryset = queryset.search(search_value)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_value = self.request.GET.get("q", "").strip()
        context["search_value"] = search_value
        if search_value:
            context["site_title"] = f"Busca por “{search_value}” - "
        else:
            context["site_title"] = "Contatos - "
        return context


class ContactDetailView(LoginRequiredMixin, DetailView):
    model = Contact
    template_name = "contact/contact_detail.html"
    context_object_name = "contact"

    def get_queryset(self):
        return Contact.objects.visible(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["site_title"] = f"{self.object.get_full_name()} - "
        return context


class ContactCreateView(LoginRequiredMixin, CreateView):
    model = Contact
    form_class = ContactForm
    template_name = "contact/contact_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["site_title"] = "Criar contato - "
        context["form_title"] = "Criar contato"
        context["form_subtitle"] = "Adicione um novo contato à sua agenda."
        context["form_submit_label"] = "Criar contato"
        context["form_action"] = reverse("contact:create")
        context["cancel_url"] = reverse("contact:index")
        return context

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, "Contato criado com sucesso.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("contact:update", args=(self.object.pk,))


class ContactUpdateView(LoginRequiredMixin, UpdateView):
    model = Contact
    form_class = ContactForm
    template_name = "contact/contact_form.html"

    def get_queryset(self):
        return Contact.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["site_title"] = "Editar contato - "
        context["form_title"] = "Editar contato"
        context["form_subtitle"] = "Atualize as informações deste contato."
        context["form_submit_label"] = "Salvar alterações"
        context["form_action"] = reverse("contact:update", args=(self.object.pk,))
        context["cancel_url"] = reverse("contact:contact", args=(self.object.pk,))
        return context

    def form_valid(self, form):
        messages.success(self.request, "Contato atualizado com sucesso.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("contact:update", args=(self.object.pk,))


class ContactDeleteView(LoginRequiredMixin, DeleteView):
    model = Contact
    template_name = "contact/contact_confirm_delete.html"
    context_object_name = "contact"
    success_url = reverse_lazy("contact:index")

    def get_queryset(self):
        return Contact.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["site_title"] = "Excluir contato - "
        return context

    def form_valid(self, form):
        messages.success(self.request, "Contato excluído com sucesso.")
        return super().form_valid(form)


class RegisterView(CreateView):
    template_name = "contact/account_form.html"
    form_class = RegisterForm
    success_url = reverse_lazy("contact:login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["site_title"] = "Criar conta - "
        context["form_title"] = "Criar conta"
        context["form_subtitle"] = "Crie sua conta para começar a usar a agenda."
        context["form_submit_label"] = "Criar conta"
        context["form_action"] = reverse("contact:register")
        return context

    def form_valid(self, form):
        messages.success(self.request, "Conta criada com sucesso. Faça o login.")
        return super().form_valid(form)


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "contact/account_form.html"
    form_class = RegisterUpdateForm
    success_url = reverse_lazy("contact:profile_update")

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["site_title"] = "Meu perfil - "
        context["form_title"] = "Meu perfil"
        context["form_subtitle"] = "Gerencie seus dados pessoais e sua senha."
        context["form_submit_label"] = "Salvar alterações"
        context["form_action"] = reverse("contact:profile_update")
        return context

    def form_valid(self, form):
        messages.success(self.request, "Perfil atualizado com sucesso.")
        return super().form_valid(form)


class UserLoginView(LoginView):
    template_name = "contact/account_form.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["site_title"] = "Entrar - "
        context["form_title"] = "Entrar"
        context["form_subtitle"] = "Bem-vindo de volta. Entre com seus dados."
        context["form_submit_label"] = "Entrar"
        context["form_action"] = reverse("contact:login")
        return context

    def get_success_url(self):
        messages.success(self.request, "Login efetuado com sucesso.")
        return super().get_success_url()


class UserLogoutView(LogoutView):
    next_page = "contact:login"

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.info(request, "Logout efetuado com sucesso.")
        return response
