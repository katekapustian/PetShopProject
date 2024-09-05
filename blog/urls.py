from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.blog, name='blog'),
    path('details/<int:post_id>/', views.blog_details, name='blog_details'),
    path('details/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('category/<slug:category_slug>/', views.blog_by_category, name='blog_by_category'),
    path('tag/<slug:tag_slug>/', views.blog_by_tag, name='blog_by_tag'),
]
