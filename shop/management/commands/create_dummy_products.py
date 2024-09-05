from django.core.management.base import BaseCommand
from shop.models import Product, FoodCategory, PetCategory, Brand
import random
from django.core.files import File
import os


class Command(BaseCommand):
    help = 'Create dummy products for testing pagination'

    def handle(self, *args, **kwargs):
        food_categories = FoodCategory.objects.all()
        pet_categories = PetCategory.objects.all()
        brands = Brand.objects.all()

        default_image_path = os.path.join('static/shop/img/product/', 'product-7.jpg')

        for i in range(100):
            food_category = random.choice(food_categories) if food_categories.exists() else None
            pet_category = random.choice(pet_categories) if pet_categories.exists() else None
            brand = random.choice(brands) if brands.exists() else None

            if not pet_category and not brand:
                pet_category = None
                brand = None
                food_category = random.choice(food_categories) if food_categories.exists() else None

            product = Product(
                name=f'Dummy Product {i+1}',
                description=f'This is a description for dummy product {i+1}.',
                new_price=random.uniform(10, 100),
                old_price=random.uniform(100, 200) if i % 2 == 0 else None,
                stock=random.randint(1, 100),
                available=True,
                food_category=food_category,
                pet_category=pet_category,
                brand=brand,
            )

            with open(default_image_path, 'rb') as img:
                product.image.save(f'dummy_image_{i+1}.jpg', File(img), save=False)

            product.save()

        self.stdout.write(self.style.SUCCESS('Successfully created 100 dummy products'))
