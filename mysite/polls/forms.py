from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import CustomUser


class CreateUserForm(UserCreationForm):
    special_number = forms.CharField(max_length=100)
    class Meta:
        model=User
        fields = ["first_name","last_name", "email", "password1", "password2"]
        # fields ="__all__"