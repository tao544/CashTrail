from django.contrib import admin
from .models import Transaction, CustomUser, SupportMessage
# Register your models here.

admin.site.register(Transaction)
admin.site.register(CustomUser)

@admin.register(SupportMessage)
class SupportMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    search_fields = ('name', 'email', 'message')
    list_filter = ('created_at',)