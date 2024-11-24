from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('reserve/', views.reserve_seat, name='reserve_seat'),  # Reservation page
    path('thank_you/', views.thank_you, name='thank_you'),  # Thank You page
    path('oauth2callback/', views.oauth2callback, name='oauth2callback'),  # Google OAuth2 callback
]