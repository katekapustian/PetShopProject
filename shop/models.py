from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User


class FoodCategory(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Food Category'
        verbose_name_plural = 'Food Categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_food_category', args=[self.slug])


class PetCategory(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Pet Category'
        verbose_name_plural = 'Pet Categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_pet_category', args=[self.slug])


class Brand(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_brand', args=[self.slug])


class Product(models.Model):
    food_category = models.ForeignKey(FoodCategory, related_name='products', on_delete=models.CASCADE)
    pet_category = models.ForeignKey(PetCategory, related_name='products', on_delete=models.CASCADE, null=True, blank=True)
    brand = models.ForeignKey(Brand, related_name='products', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, blank=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    ingredients = models.TextField(blank=True)
    new_price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telephone = models.CharField(max_length=20, blank=True)
    fax = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'
