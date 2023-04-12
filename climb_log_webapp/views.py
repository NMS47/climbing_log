from django.shortcuts import render, get_object_or_404
from datetime import datetime
from .models import Users
from django.http import Http404, HttpResponseRedirect
from .forms import SignUpForm


grades_list = [[['V'],['V0', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8', 'V9', 'V10', 'V11', 'V12', 'V13', 'V14', 'V15']],
              [['FR'],['5', '5+', '6a', '6a+', '6b', '6b+', '6c', '6c+', '7a', '7a+', '7b', '7b+', '7c', '8a', '8a+', '8b', '8b+', '8c','8c+']],
               [['Color'],['Verde', 'Azul', 'Amarillo', 'Naranja', 'Rojo', 'Negro']]] 


def home(request):
    return render(request, 'climb_log_webapp_ES/home.html')

def new_entry(request):
    return render(request, 'climb_log_webapp_ES/new_entry.html', {'grades_list': grades_list,
                                                                  'date_today':(datetime.today().strftime('%Y-%m-%d')),
                                                                  'attempts': [i for i in range(1,9)]})

def login(request):
    return render(request, 'climb_log_webapp_ES/login.html')

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        print('1')
        if form.is_valid():
            if form.cleaned_data['user_pw'] == request.POST['verify_pw']:
                print('success')
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
        print('3')

    return render(request, 'climb_log_webapp_ES/sign_up.html', {'form':form, 'verify_pw_error':verify_pw_error})

def successful_sign_up(request):
    return render(request, 'climb_log_webapp_ES/successful_sign_up.html')

def user_page(request):
    user = next(user for users in user_id if users_name['user_name']== user_name)
    pass

def users(request):
    users = Users.objects.all()
    return render(request, 'climb_log_webapp_ES/users.html', {'users':users})