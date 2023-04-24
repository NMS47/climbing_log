from django import forms
from .models import Climb_entry
from datetime import datetime

        
class NewEntryForm(forms.ModelForm):
    class Meta:
        NUM_CHOICES = [i for i in range(1,9)]

        model = Climb_entry
        exclude = ['username', 'place_coor', 'date_of_entry']
        # labels = {
        #     'date_of_climb': 'Fecha del pegue:',
        #     'place_name' : 'Lugar:',
        #     'enviroment' : 'Entorno:',
        #     'climb_style' : 'Estilo:',
        #     'multipitches' : 'Largos:',
        #     'num_pitches' : 'Nro Largos:',
        #     'grade' : 'Grado:',
        #     'climber_position' : 'Posicion:',
        #     'ascent_type' : 'Tipo de encadene:',
        #     'num_attempts' : 'Intentos:',
        #     'notes' : 'Notas:',
        # }
        # widgets = {
        #     'date_of_climb': forms.DateInput(attrs={'max':datetime.now().date(), 'id':'aloha'}),
        #     'num-pitches': forms.ChoiceField(choices=[NUM_CHOICES], required=False)
        # }
        # error_messages = 'Por favor asegurate de completar todos los campos'
        