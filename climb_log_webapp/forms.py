from django import forms
from .models import ClimbEntry
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import smtplib

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
        
class ContactForm(forms.Form):
    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'

    def send_email(self, name: str, email: str, message: str):
        email1 = "mantecasalvadores@yahoo.com"
        pw1 = 'eoufscvxmavcrcfm'
        email2 = 'nicolas.salvadores93@gmail.com'
        with smtplib.SMTP('smtp.mail.yahoo.com', 587) as connect_1:
            connect_1.starttls()
            connect_1.login(user=email1, password=pw1)
            connect_1.sendmail(from_addr=email1,
                                to_addrs=email2,
                                msg=f"Subject:CLIMBING-LOG--CONTACTO DE {name}\n\n{message}\n\nEmail: {email}")
            return print('Email sent succesfully')
        
