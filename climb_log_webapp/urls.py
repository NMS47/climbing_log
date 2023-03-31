from . import views
from django.urls import path

urlpatterns = [
	path('', views.home, name='homepage'),
    path('add_new_entry', views.new_entry, name='new-entry-form')
]