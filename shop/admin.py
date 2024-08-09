from django.contrib import admin
from .models import Product, FoodCategory, PetCategory, Brand


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'food_category', 'pet_category', 'brand', 'new_price', 'old_price', 'stock', 'available', 'created', 'updated')
    list_filter = ('available', 'created', 'updated', 'food_category', 'pet_category', 'brand')
    list_editable = ('new_price', 'old_price', 'stock', 'available')
    prepopulated_fields = {'slug': ('name',)}


class FoodCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


class PetCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Product, ProductAdmin)
admin.site.register(FoodCategory, FoodCategoryAdmin)
admin.site.register(PetCategory, PetCategoryAdmin)
admin.site.register(Brand, BrandAdmin)
