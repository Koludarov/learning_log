"""Start user's side"""

from django.urls import path, include

from . import views


app_name = 'users'

urlpatterns = [
    # Include user's auth as default
    path('', include('django.contrib.auth.urls')),
    # Registration page
    path('register/', views.register, name='register'),
]
