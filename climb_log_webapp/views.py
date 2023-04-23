from django.shortcuts import render, get_object_or_404
from datetime import datetime
from .models import User, Climb_entry
from django.http import Http404, HttpResponseRedirect
from .forms import SignUpForm
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy


grades_list = [[['V'],['V0', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8', 'V9', 'V10', 'V11', 'V12', 'V13', 'V14', 'V15']],
              [['FR'],['5', '5+', '6a', '6a+', '6b', '6b+', '6c', '6c+', '7a', '7a+', '7b', '7b+', '7c', '8a', '8a+', '8b', '8b+', '8c','8c+']],
               [['Color'],['verde', 'azul', 'amarillo', 'naranja', 'rojo', 'negro']]] 

class HomeView(TemplateView):
    template_name = 'climb_log_webapp_ES/home.html'

# def home(request):
#     return render(request, 'climb_log_webapp_ES/home.html')

def new_entry(request):
    numbers = [i for i in range(1,9)]

    if request.method =='POST':
        #    try:
            add_new_entry= Climb_entry(
            # username = User.objects.get(username='nms47'),
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

def login(request):
    return render(request, 'climb_log_webapp_ES/login.html')

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['user_pw'] == request.POST['verify_pw']:
                new_username = Users(
                    username = form.cleaned_data['username'],
                    age = form.cleaned_data['age'],
                    gender = form.cleaned_data['gender'],
                    email = form.cleaned_data['email'],
                    user_pw =form.cleaned_data['user_pw'],
                    )
                new_username.save()
                return HttpResponseRedirect("/successful_sign_up")
            else:
                verify_pw_error = True
    else:
        verify_pw_error = False
        form = SignUpForm()

    return render(request, 'climb_log_webapp_ES/sign_up.html', {'form':form, 'verify_pw_error':verify_pw_error})

def successful_sign_up(request):
    return render(request, 'climb_log_webapp_ES/successful_sign_up.html')


def user_page(request):
    user = next(user for users in user_id if users_name['user_name']== user_name)
    pass

def users(request):
    users = User.objects.all()
    return render(request, 'climb_log_webapp_ES/users.html', {'users':users})

class SuccessfulNewEntry(ListView):
    template_name = 'climb_log_webapp_ES/successful_new_entry.html'
    model = Climb_entry
    context_object_name = 'entries'

    def get_queryset(self):
        user_entries = super().get_queryset()
        data = user_entries.filter(username_id='3')
        return data
    
class EntryDetail(DetailView):
    template_name= 'climb_log_webapp_ES/entry_detail.html'
    model = Climb_entry
    context_object_name = 'entry'

class EntryList(ListView):
    template_name= 'climb_log_webapp_ES/entry_list.html'
    model = Climb_entry
    context_object_name = 'entries'


# class SignUp(CreateView):
#     model = Users
#     form_class = SignUpForm
#     template_name = 'climb_log_webapp_ES/sign_up.html'
#     success_url = 'climb_log_webapp_ES/successful_sign_up.html'
