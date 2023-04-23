from . import views
from django.urls import path

urlpatterns = [
	path('', views.HomeView.as_view(), name='homepage'),
    path('add_new_entry', views.new_entry, name='new-entry-form'),
    path('login', views.login, name='login'),
    path('sign_up/', views.sign_up, name='sign-up'),
    path('users',views.users, name='users'),
    path('successful_sign_up', views.successful_sign_up, name='successful_sign_up'),
    path('successful_new_entry', views.SuccessfulNewEntry.as_view(), name='successful-new-entry'),
    path('entry_detail/<int:pk>', views.EntryDetail.as_view(), name='entry-detail'),
    path('entry_list', views.EntryList.as_view(), name='entry-list')
]