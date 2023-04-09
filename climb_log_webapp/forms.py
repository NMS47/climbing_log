from django import forms
from .models import Users

class SignUpForm(forms.ModelForm):
    class Meta:
        model = Users
        exclude = ['id','creation_date']
        labels = {
            "username": "Elige tu nombre de usuario:",
            "email": "Email:",
            "age": "Tu edad:",
            "gender": "Tu genero:",
            "user_pw": "Elije una contrasena:"
        }