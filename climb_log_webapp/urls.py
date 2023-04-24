from . import views
from django.urls import path
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='homepage'), name='logout'),
    path('sign_up/', views.SignUpView.as_view(), name='sign-up'),

	path('', views.HomeView.as_view(), name='homepage'),
    path('entry_list/', views.EntryList.as_view(), name='entry-list'),

    path('entry_detail/<int:pk>', views.EntryDetail.as_view(), name='entry-detail'),
    path('add_new_entry/', views.NewEntryView.as_view(), name='new-entry-form'),
    path('entry_update/<int:pk>', views.EntryUpdate.as_view(), name='entry-update'),
    path('entry_delete/<int:pk>', views.EntryDelete.as_view(), name='entry-delete'),
    path('successful_sign_up/', views.SuccessfulSignUp.as_view(), name='successful-sign-up'),
    path('successful_new_entry/', views.SuccessfulNewEntry.as_view(), name='successful-new-entry'),
]