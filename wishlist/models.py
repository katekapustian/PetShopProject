from django.conf import settings
from django.db import models
from shop.models import Product


class WishlistItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} in {self.user.username}'s wishlist"

    def subtotal(self):
        return self.quantity * self.product.new_price
