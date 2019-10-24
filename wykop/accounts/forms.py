from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.forms import Form
from django.forms.fields import BooleanField

from wykop.accounts.models import User


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",)
        field_classes = {'username': UsernameField}

class ConfirmTOSForm(Form):
    confirm = BooleanField(required=True)