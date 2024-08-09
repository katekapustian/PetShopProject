from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about-us/', views.about_us, name='about_us'),
    path('contact/', views.contact, name='contact'),
    path('login-register/', views.login_register, name='login_register'),
    path('my-account/', views.my_account, name='my_account'),
    path('shop-page/', views.shop_page, name='shop_page'),
    path('shop-page/<str:category_type>/<slug:category_slug>/', views.shop_page, name='shop_page_by_category'),
    path('shop-list/', views.shop_list, name='shop_list'),
    path('shop-list/<str:category_type>/<slug:category_slug>/', views.shop_list, name='shop_list_by_category'),
    path('product/<int:id>/<slug:slug>/', views.product_details, name='product_detail'),
    path('food-category/<slug:category_slug>/', views.product_list_by_food_category,
         name='product_list_by_food_category'),
    path('pet-category/<slug:category_slug>/', views.product_list_by_pet_category, name='product_list_by_pet_category'),
    path('brand/<slug:brand_slug>/', views.product_list_by_brand, name='product_list_by_brand'),
    path('search/', views.search_products, name='search_products'),
    path('wishlist/', views.wishlist, name='wishlist'),
]
