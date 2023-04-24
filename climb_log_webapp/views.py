from django.shortcuts import render, redirect
from datetime import datetime
from .models import User, Climb_entry
from django.http import Http404, HttpResponseRedirect
from .forms import SignUpForm
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

grades_list = [[['V'],['V0', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8', 'V9', 'V10', 'V11', 'V12', 'V13', 'V14', 'V15']],
              [['FR'],['5', '5+', '6a', '6a+', '6b', '6b+', '6c', '6c+', '7a', '7a+', '7b', '7b+', '7c', '8a', '8a+', '8b', '8b+', '8c','8c+']],
               [['Color'],['verde', 'azul', 'amarillo', 'naranja', 'rojo', 'negro']]] 

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('entry-list')
    
class SignUpView(FormView):
    form_class = UserCreationForm
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


def new_entry(request):
    numbers = [i for i in range(1,9)]

    if request.method =='POST':
        #    try:
            add_new_entry= Climb_entry(
            username_id = request.user.id,
            date_of_climb = request.POST.get('date'),
            place_name = request.POST['place'],
            place_coord = 'xxxx',
            enviroment = request.POST['enviroment'],
            climb_style = request.POST['climb-style'],
            multipitches = request.POST['pitches'],
            num_pitches = request.POST['num-pitches'],
            grade = request.POST['grade'],
            climber_position = request.POST['climber-position'],
            ascent_type = request.POST['ascent-type'],
            num_attempts = request.POST['num-attempts'],
            notes = request.POST['notes']
            )
            print(request.POST['grade'])
            add_new_entry.save()
            return HttpResponseRedirect("/successful_new_entry")
        # #    except:
        #     return render(request, 'climb_log_webapp_ES/new_entry.html', {'grades_list': grades_list,
        #                         'date_today':(datetime.today().strftime('%Y-%m-%d')),
        #                         'attempts': numbers,
        #                         'error':True})
               
    return render(request, 'climb_log_webapp_ES/new_entry.html', {'grades_list': grades_list,
                                                                  'date_today':(datetime.today().strftime('%Y-%m-%d')),
                                                                  'attempts': numbers,
                                                                  'error':False}
                                                                  )

# def sign_up(request):
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             if form.cleaned_data['user_pw'] == request.POST['verify_pw']:
#                 new_username = Users(
#                     username = form.cleaned_data['username'],
#                     age = form.cleaned_data['age'],
#                     gender = form.cleaned_data['gender'],
#                     email = form.cleaned_data['email'],
#                     user_pw =form.cleaned_data['user_pw'],
#                     )
#                 new_username.save()
#                 return HttpResponseRedirect("/successful_sign_up")
#             else:
#                 verify_pw_error = True
#     else:
#         verify_pw_error = False
#         form = SignUpForm()

#     return render(request, 'climb_log_webapp_ES/sign_up.html', {'form':form, 'verify_pw_error':verify_pw_error})

class SuccessfulSignUp(TemplateView):
    template_name = 'climb_log_webapp_ES/successful_sign_up.html'

# def successful_sign_up(request):
#     return render(request, 'climb_log_webapp_ES/successful_sign_up.html')


class SuccessfulNewEntry(LoginRequiredMixin, ListView):
    template_name = 'climb_log_webapp_ES/successful_new_entry.html'
    model = Climb_entry
    context_object_name = 'entries'

    def get_queryset(self):
        user_entries = super().get_queryset()
        data = user_entries.filter(username=self.request.user)
        return data
    
class EntryList(LoginRequiredMixin, ListView):
    template_name= 'climb_log_webapp_ES/entry_list.html'
    model = Climb_entry
    context_object_name = 'entries'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["entries"] = context['entries'].filter(username_id=self.request.user.id)
        return context
    
class EntryDetail(LoginRequiredMixin, DetailView):
    template_name= 'climb_log_webapp_ES/entry_detail.html'
    model = Climb_entry
    context_object_name = 'entry'

class EntryUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'climb_log_webapp_ES/entry_update.html'
    model = Climb_entry
    fields = "__all__"
    context_object_name = 'entry'
    success_url = reverse_lazy('entry-list')

class EntryDelete(LoginRequiredMixin, DeleteView):
    template_name = 'climb_log_webapp_ES/entry_confirm_delete.html'
    model = Climb_entry
    context_object_name = 'entry'
    success_url = reverse_lazy('entry-list')


