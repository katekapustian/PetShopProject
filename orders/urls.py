from django.urls import path
from . import views
from .views import save_guest_info

app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('created/', views.order_created, name='order_created'),
    path('save-guest-info/', save_guest_info, name='save_guest_info'),
]
