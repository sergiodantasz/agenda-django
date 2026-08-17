from django.urls import path

from contact import views

app_name = "contact"

urlpatterns = [
    path("", views.ContactListView.as_view(), name="index"),
    path("search/", views.ContactListView.as_view(), name="search"),
    path("contacts/create/", views.ContactCreateView.as_view(), name="create"),
    path("contacts/<int:pk>/", views.ContactDetailView.as_view(), name="contact"),
    path(
        "contacts/<int:pk>/update/",
        views.ContactUpdateView.as_view(),
        name="update",
    ),
    path(
        "contacts/<int:pk>/delete/",
        views.ContactDeleteView.as_view(),
        name="delete",
    ),
    path("accounts/register/", views.RegisterView.as_view(), name="register"),
    path("accounts/login/", views.UserLoginView.as_view(), name="login"),
    path("accounts/logout/", views.UserLogoutView.as_view(), name="logout"),
    path("accounts/profile/", views.ProfileUpdateView.as_view(), name="profile_update"),
]
