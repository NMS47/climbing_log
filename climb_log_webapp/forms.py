from django import forms
from .models import Climb_entry
from datetime import datetime

        
class NewEntryForm(forms.ModelForm):
    class Meta:
        model = Climb_entry
        fields = "__all__"


class UpdateEntryForm(forms.ModelForm):
    class Meta:
        model = Climb_entry
        exclude = ('username',)
        