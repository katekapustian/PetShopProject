from .models import FoodCategory, PetCategory, Brand


def categories_context(request):
    return {
        'food_categories': FoodCategory.objects.all(),
        'pet_categories': PetCategory.objects.all(),
        'brands': Brand.objects.all(),
    }
