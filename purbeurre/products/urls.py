from django.urls import path

from . import views

app_name = "products"
urlpatterns = [
    # path('registration/', include('django.contrib.auth.urls')),
    path("search/", views.search_product, name="search"),
    path("info/", views.info_product, name="productinfo"),
    path("save/", views.save_favorite, name="savefavorite"),
    path("favorites/", views.show_favorite, name="displayfavorite"),
]
