from django.contrib import admin

from home_page.models import Contact, Newsletter


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "subject", "created_date"]
    search_fields = ["name", "email", "subject"]


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ["email", "joined_date"]
    search_fields = [
        "email",
    ]
    filter = ["joined_date", "email"]
