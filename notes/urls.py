from django.urls import path
from .views import *
import django.contrib.auth.views as auth_views

app_name = 'notes'

urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='notes/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='notes/loggedout.html'), name='logout'),
    path('home/', home_page, name='home_page'),
    path('update/<int:pk>/', NoteUpdateView.as_view(), name='update'),
    path('register/', register, name='register'),
    path('settings/', AccountSettingsView.as_view(), name='settings'),
    path('delete/<int:pk>/', NoteDeleteView.as_view(), name='delete')
]
