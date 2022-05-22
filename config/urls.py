"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from purbeurre.home.views import HomeView, LegalView
from purbeurre.accounts.views import login_user, logout_user, register_user, profile
from purbeurre.products.views import info_product, search_product, save_favorite
from purbeurre.products.views import show_favorite

app_name = 'config'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('registration/', include('django.contrib.auth.urls')),
    path('register/', register_user, name='register'),
    path('profile/', profile, name='profile'),
    path('search/', search_product, name='search'),
    path('product/', info_product, name="product"),
    path('save/',save_favorite, name='savefavorite'),
    path('favorites/', show_favorite, name='displayfavorite'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('legal/', LegalView.as_view(), name='legal')
]