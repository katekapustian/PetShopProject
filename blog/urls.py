from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog, name='blog'),
    path('details/', views.blog_details, name='blog_details'),
    path('leftsidebar/', views.blog_leftsidebar, name='blog_leftsidebar'),
]
