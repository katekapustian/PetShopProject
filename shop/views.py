from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.http import url_has_allowed_host_and_scheme
from .models import Product, FoodCategory, PetCategory, Brand, Profile, NewsletterSubscription
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm, AddressUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .utils import ensure_profile_exists
from django.http import JsonResponse
from django.utils.text import Truncator
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


def index(request):
    latest_products = Product.objects.filter(available=True).order_by('-created')[:8]
    context = {
        'latest_products': latest_products,
    }
    return render(request, 'shop/index.html', context)


def about_us(request):
    return render(request, 'shop/about-us.html')


def contact(request):
    return render(request, 'shop/contact.html')


def login_register(request):
    return render(request, 'shop/login-register.html')


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            messages.success(request, 'Registration successful. Please log in.')
            return redirect('shop:login_register')
        else:
            register_errors = form.errors.get_json_data()
            formatted_errors = []
            for field, errors in register_errors.items():
                for error in errors:
                    formatted_errors.append(f"{field}: {error['message']}")
            return render(request, 'shop/login-register.html', {'register_errors': formatted_errors})
    return redirect('shop:login_register')


def login(request):
    next_url = request.GET.get('next', 'shop:index')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                if url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                    return HttpResponseRedirect(next_url)
                else:
                    return redirect('shop:index')
            else:
                login_errors = 'Incorrect username or password.'
                return render(request, 'shop/login-register.html', {'form': form, 'login_errors': login_errors, 'next': next_url})
        else:
            login_errors = 'Incorrect username or password.'
            return render(request, 'shop/login-register.html', {'form': form, 'login_errors': login_errors, 'next': next_url})
    else:
        form = AuthenticationForm()
        return render(request, 'shop/login-register.html', {'form': form, 'next': next_url})


@login_required
def my_account(request):
    ensure_profile_exists(request.user)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        address_form = AddressUpdateForm(request.POST, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid() and address_form.is_valid():
            user_form.save()
            profile_form.save()
            address_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('shop:my_account')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
        address_form = AddressUpdateForm(instance=request.user.profile)

    countries = ["United States", "Ukraine", "United Kingdom"]
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'address_form': address_form,
        'countries': countries
    }

    return render(request, 'shop/my-account.html', context)


@login_required
def update_account(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your account information has been updated!')
            return redirect('shop:my_account')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }

    return render(request, 'shop/update-account.html', context)


@login_required
def update_address(request):
    if request.method == 'POST':
        address_form = AddressUpdateForm(request.POST, instance=request.user.profile)
        if address_form.is_valid():
            address_form.save()
            messages.success(request, 'Your address has been updated!')
            return redirect('shop:my_account')
    else:
        address_form = AddressUpdateForm(instance=request.user.profile)

    countries = ["United States", "Ukraine", "United Kingdom"]
    context = {
        'address_form': address_form,
        'countries': countries,
    }

    return render(request, 'shop/update-address.html', context)


@login_required
def logout_view(request):
    next_url = request.GET.get('next', 'shop:index')
    if url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        logout(request)
        return HttpResponseRedirect(next_url)
    else:
        logout(request)
        return redirect('shop:index')


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


def quick_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    truncated_description = Truncator(product.description).chars(500, truncate='...')

    data = {
        'name': product.name,
        'new_price': product.new_price,
        'description': truncated_description,
        'full_description_url': product.get_absolute_url(),
        'image_url': product.image.url
    }
    return JsonResponse(data)


def subscribe_newsletter(request):
    if request.method == 'POST':
        email = request.POST.get('EMAIL')

        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Please enter a valid email address.", extra_tags='error')
            return redirect('shop:index')

        if NewsletterSubscription.objects.filter(email=email).exists():
            messages.error(request, "This email is already subscribed.", extra_tags='error')
        else:
            subscription = NewsletterSubscription(email=email)
            subscription.save()
            messages.success(request, "Thanks for subscribing!", extra_tags='success')

        return redirect('shop:index')
