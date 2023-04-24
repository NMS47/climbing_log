from . import views
from django.urls import path
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login', views.CustomLoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(next_page='homepage'), name='logout'),
	path('', views.HomeView.as_view(), name='homepage'),
    path('add_new_entry', views.new_entry, name='new-entry-form'),
    path('sign_up/', views.sign_up, name='sign-up'),
    path('users',views.users, name='users'),
    path('successful_sign_up', views.successful_sign_up, name='successful_sign_up'),
    path('successful_new_entry', views.SuccessfulNewEntry.as_view(), name='successful-new-entry'),
    path('entry_detail/<int:pk>', views.EntryDetail.as_view(), name='entry-detail'),
    path('entry_list', views.EntryList.as_view(), name='entry-list'),
    path('entry_update/<int:pk>', views.EntryUpdate.as_view(), name='entry-update'),
    path('entry_delete/<int:pk>', views.EntryDelete.as_view(), name='entry-delete'),
]