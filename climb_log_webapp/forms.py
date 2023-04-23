from django import forms
from .models import User

class SignUpForm(forms.ModelForm):

    class Meta:
        model = User
        exclude = ['id','creation_date']
        labels = {
            "username": "Elige tu nombre de usuario:",
            "email": "Email:",
            "age": "Tu edad:",
            "gender": "Tu género:",
            "user_pw": "Elije una contraseña:" 
        }
        widgets = {
            'user_pw': forms.PasswordInput()
        }
        error_messages = 'Las contraseñas no coinciden, intenta de nuevo.'
        
        