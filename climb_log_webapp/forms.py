from django import forms
from .models import Climb_entry

        
class NewEntryForm(forms.ModelForm):
    class Meta:
        model = Climb_entry
        exclude = ['username', 'place_coor', 'date_of_entry']
        labels = {
            'date_of_climb': 'Fecha del pegue:',
            'place_name' : 'Lugar:',
            'enviroment' : 'Entorno:',
            'climb_style' : 'Estilo:',
            'multipitches' : 'Largos:',
            'num_pitches' : 'Nro Largos:',
            'grade' : 'Grado:',
            'climber_position' : 'Posicion:',
            'ascent_type' : 'Tipo de encadene:',
            'num_attempts' : 'Intentos:',
            'notes' : 'Notas:',
        }
        widgets = {
            'user_pw': forms.PasswordInput()
        }
        error_messages = 'Por favor asegurate de completar todos los campos'
        