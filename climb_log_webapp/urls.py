from . import views
from django.urls import path

urlpatterns = [
	path('', views.home, name='homepage'),
    path('add_new_entry', views.new_entry, name='new-entry-form'),
    path('login', views.login, name='login'),
    path('sign_up', views.sign_up, name='sign-up'),
]