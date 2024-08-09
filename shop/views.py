from django.shortcuts import render, get_object_or_404
from .models import Product, FoodCategory, PetCategory, Brand
from django.core.paginator import Paginator
from django.db.models import Q


def index(request):
    return render(request, 'shop/index.html')


def about_us(request):
    return render(request, 'shop/about-us.html')


def contact(request):
    return render(request, 'shop/contact.html')


def login_register(request):
    return render(request, 'shop/login-register.html')


def my_account(request):
    return render(request, 'shop/my-account.html')


def product_details(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    categories = []
    if product.food_category:
        categories.append(product.food_category.name)
    if product.pet_category:
        categories.append(product.pet_category.name)
    if product.brand:
        categories.append(product.brand.name)
    categories_string = " / ".join(categories)

    return render(request, 'shop/product-details.html', {
        'product': product,
        'categories_string': categories_string
    })


def shop_list(request, category_slug=None, category_type=None):
    food_categories = FoodCategory.objects.all()
    pet_categories = PetCategory.objects.all()
    brands = Brand.objects.all()
    products = Product.objects.filter(available=True)
    current_category = None

    if category_slug and category_type:
        if category_type == 'food':
            current_category = get_object_or_404(FoodCategory, slug=category_slug)
            products = products.filter(food_category=current_category)
        elif category_type == 'pet':
            current_category = get_object_or_404(PetCategory, slug=category_slug)
            products = products.filter(pet_category=current_category)
        elif category_type == 'brand':
            current_category = get_object_or_404(Brand, slug=category_slug)
            products = products.filter(brand=current_category)

    num_products_per_page = int(request.GET.get('num_products_per_page', 6))

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price and max_price:
        products = products.filter(new_price__gte=min_price, new_price__lte=max_price)

    paginator = Paginator(products, num_products_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'shop/shop-list.html', {
        'current_category': current_category,
        'category_type': category_type,
        'food_categories': food_categories,
        'pet_categories': pet_categories,
        'brands': brands,
        'products': page_obj,
        'num_products_per_page': num_products_per_page,
        'paginator': paginator,
        'page_obj': page_obj,
    })


def shop_page(request, category_slug=None, category_type=None):
    food_categories = FoodCategory.objects.all()
    pet_categories = PetCategory.objects.all()
    brands = Brand.objects.all()
    products = Product.objects.filter(available=True)
    current_category = None

    if category_slug and category_type:
        if category_type == 'food':
            current_category = get_object_or_404(FoodCategory, slug=category_slug)
            products = products.filter(food_category=current_category)
        elif category_type == 'pet':
            current_category = get_object_or_404(PetCategory, slug=category_slug)
            products = products.filter(pet_category=current_category)
        elif category_type == 'brand':
            current_category = get_object_or_404(Brand, slug=category_slug)
            products = products.filter(brand=current_category)

    num_products_per_page = int(request.GET.get('num_products_per_page', 6))

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price and max_price:
        products = products.filter(new_price__gte=min_price, new_price__lte=max_price)

    paginator = Paginator(products, num_products_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'shop/shop-page.html', {
        'current_category': current_category,
        'category_type': category_type,
        'food_categories': food_categories,
        'pet_categories': pet_categories,
        'brands': brands,
        'products': page_obj,
        'num_products_per_page': num_products_per_page,
        'paginator': paginator,
        'page_obj': page_obj,
    })


def wishlist(request):
    return render(request, 'shop/wishlist.html')


def product_list_by_food_category(request, category_slug=None):
    food_category = None
    food_categories = FoodCategory.objects.all()
    pet_categories = PetCategory.objects.all()
    brands = Brand.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        food_category = get_object_or_404(FoodCategory, slug=category_slug)
        products = products.filter(food_category=food_category)
    return render(request, 'shop/shop-page.html', {
        'food_category': food_category,
        'food_categories': food_categories,
        'pet_categories': pet_categories,
        'brands': brands,
        'products': products
    })


def product_list_by_pet_category(request, category_slug=None):
    pet_category = None
    food_categories = FoodCategory.objects.all()
    pet_categories = PetCategory.objects.all()
    brands = Brand.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        pet_category = get_object_or_404(PetCategory, slug=category_slug)
        products = products.filter(pet_category=pet_category)
    return render(request, 'shop/shop-page.html', {
        'pet_category': pet_category,
        'food_categories': food_categories,
        'pet_categories': pet_categories,
        'brands': brands,
        'products': products
    })


def product_list_by_brand(request, brand_slug=None):
    brand = None
    food_categories = FoodCategory.objects.all()
    pet_categories = PetCategory.objects.all()
    brands = Brand.objects.all()
    products = Product.objects.filter(available=True)
    if brand_slug:
        brand = get_object_or_404(Brand, slug=brand_slug)
        products = products.filter(brand=brand)
    return render(request, 'shop/shop-page.html', {
        'brand': brand,
        'food_categories': food_categories,
        'pet_categories': pet_categories,
        'brands': brands,
        'products': products
    })


def search_products(request):
    food_categories = FoodCategory.objects.all()
    pet_categories = PetCategory.objects.all()
    brands = Brand.objects.all()
    products = Product.objects.filter(available=True)
    query = request.GET.get('q')

    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    num_products_per_page = int(request.GET.get('num_products_per_page', 6))

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price and max_price:
        products = products.filter(new_price__gte=min_price, new_price__lte=max_price)

    paginator = Paginator(products, num_products_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    view_type = request.GET.get('view_type', 'grid')
    template_name = 'shop/shop-list.html' if view_type == 'list' else 'shop/shop-page.html'

    return render(request, template_name, {
        'food_categories': food_categories,
        'pet_categories': pet_categories,
        'brands': brands,
        'products': page_obj,
        'num_products_per_page': num_products_per_page,
        'paginator': paginator,
        'page_obj': page_obj,
        'query': query,
        'search_mode': True,
    })
