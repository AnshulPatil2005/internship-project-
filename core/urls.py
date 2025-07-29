#contains URL patterns for the core application
# core/urls.py
# This file contains URL patterns for user authentication, client management, and video handling.
# It maps URLs to views and includes necessary static file handling.
#the tempelate name here points to the login template in the html directory
# Ensure to import necessary views and settings from Django.
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register, name='register'),
    path('', views.home, name='home'),
    path('add-client/', views.add_client, name='add_client'),
    path('clients/', views.list_clients, name='list_clients'),
    path('delete-client/<int:client_id>/', views.delete_client, name='delete_client'),
    path('videos/', views.list_videos, name='list_videos'),
    path('upload-video/', views.upload_video, name='upload_video'),
    path('map/', views.show_map, name='show_map'),
    path('show-signals/', views.show_all_signals, name='show_signals'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
