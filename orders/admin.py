from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'address', 'total_price', 'paid', 'created', 'updated']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]

    def total_price(self, obj):
        return "${:.2f}".format(sum(item.price * item.quantity for item in obj.items.all()))

    total_price.short_description = 'Total Price'


admin.site.register(Order, OrderAdmin)
