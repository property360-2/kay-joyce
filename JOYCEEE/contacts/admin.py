# contacts/admin.py
from django.contrib import admin
from .models import Contact

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'category']
    list_filter = ['category']
    search_fields = ['name', 'phone', 'email']