from django.urls import path

from home.views import HomeView, LegalView
from .import views

app_name = 'home'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('legal/', LegalView.as_view(), name='legal'),
    path('password_reset', views.password_reset_request, name="password_reset")
]
