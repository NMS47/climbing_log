from django.shortcuts import render
from datetime import datetime


grades_list = ['V0', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8', 'V9', 'V10', 'V11', 'V12', 'V13', 'V14', 'V15', '5', '5+', '6a', '6a+', '6b', '6b+', '6c', '6c+', '7a', '7a+', '7b', '7b+', '7c', '8a', '8a+', '8b']


def home(request):
    return render(request, 'climb_log_webapp_ES/home.html')

def new_entry(request):
    return render(request, 'climb_log_webapp_ES/new_entry.html', {'grades_list': grades_list,
                                                                  'date_today':(datetime.today().strftime('%Y-%m-%d'))})

def login(request):
    return render(request, 'climb_log_webapp_ES/login.html')

def sign_up(request):
    return render(request, 'climb_log_webapp_ES/sign_up.html')