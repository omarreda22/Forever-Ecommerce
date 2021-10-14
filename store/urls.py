from django.urls import path
from . import views

app_name = "store"

urlpatterns = [
    path('', views.store, name='store'),
    path('/<slug:category_slug>/', views.store, name='categries'),
    path('/<slug:category_slug>/<slug:product_details_slug>/', views.product_details, name='product_details'),
]
