from django.contrib import admin

from contact import models


@admin.register(models.Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "get_full_name",
        "phone",
        "email",
        "category",
        "owner",
        "created_date",
        "show",
    )
    list_display_links = ("id", "get_full_name")
    list_filter = ("category", "owner", "show", "created_date")
    list_editable = ("show",)
    search_fields = ("first_name", "last_name", "phone", "email")
    date_hierarchy = "created_date"
    ordering = ("-id",)
    list_per_page = 25
    readonly_fields = ("created_date",)


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "picture")
    search_fields = (
        "user__username",
        "user__first_name",
        "user__last_name",
        "user__email",
    )


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "contact_count")
    ordering = ("name",)

    @admin.display(description="Contatos")
    def contact_count(self, obj):
        return obj.contacts.count()
