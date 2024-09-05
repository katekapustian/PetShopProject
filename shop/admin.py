from django.contrib import admin
from .models import Product, FoodCategory, PetCategory, Brand, Profile, NewsletterSubscription, Review, DealOfTheWeek, \
    ContactMessage
from django.contrib.auth.models import User


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'food_category', 'pet_category', 'brand', 'new_price', 'old_price',
                    'stock', 'available', 'created', 'updated')
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


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_first_name', 'get_last_name', 'telephone', 'fax',
                    'address', 'city', 'zip_code', 'country')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'telephone', 'fax',
                     'address', 'city', 'zip_code', 'country')
    list_filter = ('country', 'city')

    def get_first_name(self, obj):
        return obj.user.first_name
    get_first_name.admin_order_field = 'user__first_name'

    get_first_name.short_description = 'First Name'

    def get_last_name(self, obj):
        return obj.user.last_name
    get_last_name.admin_order_field = 'user__last_name'
    get_last_name.short_description = 'Last Name'


@admin.register(NewsletterSubscription)
class NewsletterSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email', 'coupon_code', 'coupon_used')
    search_fields = ('email', 'coupon_code')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'first_name', 'last_name', 'rating', 'created_at')
    search_fields = ('product__name', 'user__username', 'first_name', 'last_name')
    list_filter = ('rating', 'created_at')


class DealOfTheWeekAdmin(admin.ModelAdmin):
    list_display = ('product', 'start_date', 'end_date', 'is_active')


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'subject', 'sent_at')
    search_fields = ('first_name', 'last_name', 'email', 'subject')
    list_filter = ('sent_at',)


admin.site.register(Product, ProductAdmin)
admin.site.register(FoodCategory, FoodCategoryAdmin)
admin.site.register(PetCategory, PetCategoryAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(DealOfTheWeek, DealOfTheWeekAdmin)
