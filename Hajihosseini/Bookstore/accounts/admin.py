from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = UserCreationForm
    form = UserChangeForm
    list_display = UserAdmin.list_display[:4] + ('nat_code', 'gender', 'phone_number') + UserAdmin.list_display[4:]
    list_display_links = UserAdmin.list_display[:4] + ('nat_code', 'gender', 'phone_number') + UserAdmin.list_display[4:]
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('nat_code', 'gender', 'phone_number')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('nat_code', 'gender', 'phone_number')}),
    )

