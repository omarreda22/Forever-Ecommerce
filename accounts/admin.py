from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Account


class AccountAdmin(UserAdmin):
    list_display = ['email', 'username','first_name', 'last_name', 'last_login' ,'is_active']
    readonly_fields = ['date_joined', 'last_login', ]
    ordering = ('-date_joined_for_format',)
    list_filter = ['is_active']


    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Account, AccountAdmin)