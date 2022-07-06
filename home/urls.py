from django.urls import path

from home.views import HomeView, LegalView

app_name = 'home'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('legal/', LegalView.as_view(), name='legal'),
]
