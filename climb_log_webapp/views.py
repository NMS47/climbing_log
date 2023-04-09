from django.shortcuts import render, get_object_or_404
from datetime import datetime
from .models import Users
from django.http import Http404, HttpResponseRedirect


grades_list = ['V0', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8', 'V9', 'V10', 'V11', 'V12', 'V13', 'V14', 'V15', '5', '5+', '6a', '6a+', '6b', '6b+', '6c', '6c+', '7a', '7a+', '7b', '7b+', '7c', '8a', '8a+', '8b']


def home(request):
    return render(request, 'climb_log_webapp_ES/home.html')

def new_entry(request):
    return render(request, 'climb_log_webapp_ES/new_entry.html', {'grades_list': grades_list,
                                                                  'date_today':(datetime.today().strftime('%Y-%m-%d'))})

def login(request):
    return render(request, 'climb_log_webapp_ES/login.html')

def sign_up(request):
    if request.method == 'POST':
        username = request.POST['username']
        age = request.POST['age']
        gender = request.POST['gender']
        email = request.POST['email']
        pw = request.POST['pw']
        return HttpResponseRedirect("/successful_sign_up")
    return render(request, 'climb_log_webapp_ES/sign_up.html')

def successful_sign_up(request):
    return render(request, 'climb_log_webapp_ES/successful_sign_up.html')

def user_page(request):
    user = next(user for users in user_id if users_name['user_name']== user_name)
    pass

def users(request):
    users = Users.objects.all()
    return render(request, 'climb_log_webapp_ES/users.html', {'users':users})