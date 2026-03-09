from django.contrib import admin
from .models import Transaction, CustomUser
# Register your models here.

admin.site.register(Transaction)
admin.site.register(CustomUser)
