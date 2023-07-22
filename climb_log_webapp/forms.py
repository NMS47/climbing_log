from django import forms
from .models import ClimbEntry
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email')


class NewEntryForm(forms.ModelForm):
    class Meta:
        model = ClimbEntry
        fields = "__all__"


class UpdateEntryForm(forms.ModelForm):
    class Meta:
        model = ClimbEntry
        exclude = ('username',)
        