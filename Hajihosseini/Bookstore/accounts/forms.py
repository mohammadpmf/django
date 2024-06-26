from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        # fields = UserCreationForm.Meta.fields + ('nat_code', 'gender', 'phone_number')
        fields = ['first_name', 'last_name', 'email', 'nat_code', 'gender', 'phone_number', 'username']

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        # fields = UserChangeForm.Meta.fields
        fields = ['username']
