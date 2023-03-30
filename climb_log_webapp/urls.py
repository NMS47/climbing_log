from . import views
from django.urls import path

urlpatterns = [
	path('', views.home, name='homepage'),
    path('new_entry', views.new_entry, name='new_entry')
]