from typing import Any, Dict
from django.http import HttpResponse
from django.shortcuts import redirect
from datetime import datetime
import smtplib
#For plotly charts
from .plots import heat_cal, style_plot, climb_map, fav_place, grade_record, progression_plot

from datetime import datetime

from .models import ClimbEntry,  ClimbPlaces
from .forms import NewEntryForm, UpdateEntryForm, UserCreateForm, ContactForm
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin


grades_list = [[['Color'],['verde', 'azul', 'amarillo', 'naranja', 'rojo', 'negro']],
               [['V'],['V0', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8', 'V9', 'V10', 'V11', 'V12', 'V13', 'V14', 'V15']],
              [['FR'],['5', '5+', '6a', '6a+', '6b', '6b+', '6c', '6c+', '7a', '7a+', '7b', '7b+', '7c', '8a', '8a+', '8b', '8b+', '8c','8c+']]
               ] 
# This is to asign a value to the grades
# grades_dict = {}
# for grade_list in grades_list:
#     category = grade_list[0][0]  # Get the category name
#     grades = grade_list[1]  # Get the list of grades
#     grades_dict[category] = {grade: i + 1 for i, grade in enumerate(grades)}
#-----------------------------------------
# grades_dict = [[['Color'],[{'verde': 1, 'azul': 2, 'amarillo': 3, 'naranja': 4, 'rojo': 5, 'negro': 6}]],
#                [['V'],[{'V0': 1, 'V1': 2, 'V2': 3, 'V3': 4, 'V4': 5, 'V5': 6, 'V6': 7, 'V7': 8, 'V8': 9, 'V9': 10, 'V10': 11, 'V11': 12, 'V12': 13, 'V13': 14, 'V14': 15, 'V15': 16}]],
#               [['FR'],[{'5': 1, '5+': 2, '6a': 3, '6a+': 4, '6b': 5, '6b+': 6, '6c': 7, '6c+': 8, '7a': 9, '7a+': 10, '7b': 11, '7b+': 12, '7c': 13, '8a': 14, '8a+': 15, '8b': 16, '8b+': 17, '8c': 18, '8c+': 19}]]
#                ] 
grades_dict={'verde': 1, 'azul': 2, 'amarillo': 3, 'naranja': 4, 'rojo': 5, 'negro': 6, 'V0': 1, 'V1': 2, 'V2': 3, 'V3': 4, 'V4': 5, 'V5': 6, 'V6': 7, 'V7': 8, 'V8': 9, 'V9': 10, 'V10': 11, 'V11': 12, 'V12': 13, 'V13': 14, 'V14': 15, 'V15': 16, '5': 1, '5+': 2, '6a': 3, '6a+': 4, '6b': 5, '6b+': 6, '6c': 7, '6c+': 8, '7a': 9, '7a+': 10, '7b': 11, '7b+': 12, '7c': 13, '8a': 14, '8a+': 15, '8b': 16, '8b+': 17, '8c': 18, '8c+': 19 }

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('entry-list')
    
class SignUpView(FormView):
    form_class = UserCreateForm
    template_name = 'registration/sign_up.html'
    
    def get_success_url(self):
        return reverse_lazy('successful-sign-up')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
            return super(SignUpView, self).form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('entry-list')
        
        return super(SignUpView, self).get(*args, **kwargs)

class HomeView(TemplateView):
    template_name = 'climb_log_webapp_ES/home.html'

class NewEntryView(LoginRequiredMixin, FormView):
    template_name = 'climb_log_webapp_ES/new_entry.html'
    form_class = NewEntryForm
    extra_context = {'multipitches': False,
                     'num_pitches': 1,
                    #  'ascent_type': 'not-specified',
                     'num_attempts': 1,
                     'date_today': datetime.today().strftime('%Y-%m-%d'),
                     'attempts': [i for i in range(1,9)],
                     'grades_list': grades_list
                                          }
    success_url =reverse_lazy('successful-new-entry')
    model = ClimbEntry

# This is to pass variables to the template 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = ClimbPlaces.objects.values_list('id','place_name')
        places_list = [[n[0],n[1]] for n in queryset.all()]
        context['places_list'] = places_list
        context['form_type'] = self.kwargs['form_type']
        return context

# This is to add a username, grade_equivalent to the climbEntry, otherwise it is not saved to db
    def form_valid(self, form):
        form.instance.grade_equivalent = grades_dict.get(form.instance.grade)
        # form.instance.ascent_type = 'not-specified'
        number_of_entries = int(self.request.POST.get('multiple_entries','')) 
        form.instance.username = self.request.user
        instance = form.save(commit=False)
        for n in range(number_of_entries):
            instance.pk = None
            instance.save()
        return super().form_valid(form)
    
class NewSessionView(LoginRequiredMixin, FormView):
    template_name = 'climb_log_webapp_ES/new_session.html'
    form_class = NewEntryForm
    extra_context = {'multipitches': False,
                     'num_pitches': 1,
                     'ascent_type': 'not-specified',
                     'num_attempts': 1,
                     'date_today': datetime.today().strftime('%Y-%m-%d'),
                     'attempts': [i for i in range(1,9)],
                     'grades_list': grades_list
                                          }
    success_url =reverse_lazy('successful-new-entry')
    model = ClimbEntry

# This is to pass variables to the template 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = ClimbPlaces.objects.values_list('id','place_name')
        places_list = [[n[0],n[1]] for n in queryset.all()]
        context['places_list'] = places_list
        return context

# This is to add a username, grade_equivalent to the climbEntry, otherwise it is not saved to db
    def form_valid(self, form):
        # Creates a dict with all the entries added by user
        result_dict = dict(zip(self.request.POST.getlist('grade'), self.request.POST.getlist('multiple_entries')))
        # Iters through the dict and asign the values needed for a single entry in the db
        for key,value in result_dict.items():
            grade_equivalent = grades_dict.get(key)
            number_of_entries = int(value)
            form.instance.grade = key
            form.instance.grade_equivalent = grade_equivalent
            form.instance.ascent_type = 'not-specified'
            form.instance.username = self.request.user
            instance = form.save(commit=False)
            for n in range(number_of_entries):
                instance.pk = None
                instance.save()
        return super().form_valid(form)
    

class SuccessfulSignUp(TemplateView):
    template_name = 'climb_log_webapp_ES/successful_sign_up.html' 


class SuccessfulNewEntry(LoginRequiredMixin, ListView):
    template_name = 'climb_log_webapp_ES/successful_new_entry.html'
    model = ClimbEntry
    context_object_name = 'entries'

    def get_queryset(self):
        user_entries = super().get_queryset()
        data = user_entries.filter(username=self.request.user)
        return data
    
class Profile(LoginRequiredMixin, ListView):
    template_name= 'climb_log_webapp_ES/profile.html'
    model = ClimbEntry
    allow_empty=False
    context_object_name = 'entries'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entries'] = context['entries'].filter(username_id=self.request.user.id)
        # catches exception where user is not logged in
        if not context['entries'].filter(username_id=self.request.user.id):
            return context
        
        #CHECK IN plots.py FOR THE ACTUAL FUNCTIONS, THIS IS JUST A SIMPLIFICATION FOR ORGANIZATION PURPOSES

        #-----------------------Heatmap calendar--------------------------------------
        context['calendar_plot'] = heat_cal(context['entries'].values('date_of_climb', 'num_pitches', 'num_attempts'))

        #--------------Styles chart----------------------------------
        context['style_chart'] = style_plot(context['entries'].values('climb_style', 'num_attempts'))

        #-------------Records------------------------------------------
        context['records'] = grade_record(context['entries'].values('date_of_climb', 'climb_style', 'grade', 'grade_equivalent'))
 
        #Fav place-----------------------------------------------------
        context['favorite_places'] = fav_place(context['entries'].values('climb_style', 'place_name__place_name'))
        
        #Progression line---------------------------------------------
        context['prog_plot'] = progression_plot(context['entries'].values('date_of_climb', 'climb_style', 'grade', 'grade_equivalent'))

        #Climbs maps----------------------------------------
        figure = climb_map(context['entries'].values('place_name__place_name', 'place_name__place_coords', 'place_name__enviroment'))
        figure.render()
        context["map"] = figure
        return context

    
class EntryList(LoginRequiredMixin, ListView):
    template_name= 'climb_log_webapp_ES/entry_list.html'
    model = ClimbEntry
    paginate_by = 15
    context_object_name = 'entries'
    
    #This is the way of filtering the db when using paginator
    def get_queryset(self):
        return ClimbEntry.objects.filter(username_id=self.request.user.id).order_by('-date_of_climb')
  
    
class EntryDetail(LoginRequiredMixin, DetailView):
    template_name= 'climb_log_webapp_ES/entry_detail.html'
    model = ClimbEntry
    context_object_name = 'entry'


class EntryUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'climb_log_webapp_ES/entry_update.html'
    model = ClimbEntry
    # Created a form class to exclude the username field
    form_class = UpdateEntryForm
    context_object_name = 'entry'
    success_url = reverse_lazy('entry-list')


class EntryDelete(LoginRequiredMixin, DeleteView):
    template_name = 'climb_log_webapp_ES/entry_confirm_delete.html'
    model = ClimbEntry
    context_object_name = 'entry'
    success_url = reverse_lazy('entry-list')
 
    
class ContactPage(FormView):
    template_name = 'climb_log_webapp_ES/contact.html' 
    form_class = ContactForm
    success_url = reverse_lazy('homepage')

    def form_valid(self, form: Any):
        form.send_email(form.cleaned_data['name'], form.cleaned_data['email'], form.cleaned_data['message'])
        return super().form_valid(form)