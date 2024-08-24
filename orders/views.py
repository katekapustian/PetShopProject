from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from .models import Order, OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from shop.models import Profile, NewsletterSubscription
from django.http import JsonResponse
import json
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


@csrf_protect
def order_create(request):
    cart = Cart(request)
    errors = []

    discount = 0
    coupon_code = None
    grand_total = cart.get_total_price()

    if len(cart) == 0:
        errors.append("Your cart is empty. Please add some products to your cart before proceeding to checkout.")
        return render(request, 'orders/checkout.html', {'cart': cart, 'errors': errors})

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        email = request.POST.get('email')

        try:
            validate_email(email)
        except ValidationError:
            errors.append("Please enter a valid email address.")
            return render(request, 'orders/checkout.html', {
                'cart': cart,
                'form': form,
                'countries': ["United States", "Ukraine", "United Kingdom"],
                'errors': errors,
                'discount': discount,
                'coupon_code': coupon_code,
                'grand_total': grand_total
            })

        if form.is_valid():
            if request.user.is_authenticated:
                profile = Profile.objects.get(user=request.user)
                grand_total = cart.get_total_price_after_discount(request.user.email)
                order = Order(
                    user=request.user,
                    first_name=request.user.first_name or '',
                    last_name=request.user.last_name or '',
                    email=request.user.email or '',
                    address=profile.address or '',
                    city=profile.city or '',
                    postal_code=profile.zip_code or '',
                    country=profile.country or '',
                    phone=profile.telephone or '',
                    fax=profile.fax or '',
                    total_price=grand_total,
                )
            else:
                grand_total = cart.get_total_price_after_discount(email)
                order = Order(
                    first_name=request.POST.get('first_name') or request.session.get('guest_first_name') or '',
                    last_name=request.POST.get('last_name') or request.session.get('guest_last_name') or '',
                    email=email or request.session.get('guest_email') or '',
                    address=form.cleaned_data['address'],
                    city=form.cleaned_data['city'],
                    postal_code=form.cleaned_data['postal_code'],
                    country=form.cleaned_data['country'],
                    phone=form.cleaned_data['phone'],
                    fax=form.cleaned_data['fax'] or '',
                    total_price=grand_total,
                )

            order.save()

            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )

            discount, coupon_code = cart.get_discount(email)
            if coupon_code:
                subscription = NewsletterSubscription.objects.get(email=email)
                subscription.coupon_used = True
                subscription.save()

            cart.clear()
            request.session['order_id'] = order.id
            return redirect('orders:order_created')
        else:
            errors += form.errors.as_data()

    else:
        if request.user.is_authenticated:
            profile = Profile.objects.get(user=request.user)
            initial_data = {
                'first_name': request.user.first_name or '',
                'last_name': request.user.last_name or '',
                'email': request.user.email or '',
                'address': profile.address or '',
                'city': profile.city or '',
                'postal_code': profile.zip_code or '',
                'country': profile.country or '',
                'phone': profile.telephone or '',
                'fax': profile.fax or '',
            }
        else:
            first_name = request.session.get('guest_first_name') or ''
            last_name = request.session.get('guest_last_name') or ''
            email = request.session.get('guest_email') or ''
            initial_data = {
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'address': request.session.get('guest_address') or '',
                'city': request.session.get('guest_city') or '',
                'postal_code': request.session.get('guest_postal_code') or '',
                'country': request.session.get('guest_country') or '',
                'phone': request.session.get('guest_phone') or '',
                'fax': request.session.get('guest_fax') or '',
            }

        form = OrderCreateForm(initial=initial_data)
        email = request.user.email if request.user.is_authenticated else request.session.get('guest_email')
        discount, coupon_code = cart.get_discount(email)
        grand_total = cart.get_total_price_after_discount(email)

    countries = ["United States", "Ukraine", "United Kingdom"]
    return render(request, 'orders/checkout.html', {
        'cart': cart,
        'form': form,
        'countries': countries,
        'errors': errors,
        'discount': discount,
        'coupon_code': coupon_code,
        'grand_total': grand_total
    })


def order_created(request):
    order_id = request.session.get('order_id')
    if not order_id:
        return redirect('cart:cart_detail')
    order = Order.objects.get(id=order_id)
    del request.session['order_id']
    return render(request, 'orders/order_created.html', {'order': order})


@csrf_exempt
def save_guest_info(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            try:
                validate_email(email)
            except ValidationError:
                return JsonResponse({'success': False, 'error': 'Invalid email address'})

            request.session['guest_first_name'] = data['first_name']
            request.session['guest_last_name'] = data['last_name']
            request.session['guest_email'] = email
            request.session['guest_address'] = data.get('address', '')
            request.session['guest_city'] = data.get('city', '')
            request.session['guest_postal_code'] = data.get('postal_code', '')
            request.session['guest_country'] = data.get('country', '')
            request.session['guest_phone'] = data.get('phone', '')
            request.session['guest_fax'] = data.get('fax', '')

            cart = Cart(request)
            discount, coupon_code = cart.get_discount(email)
            subtotal = cart.get_total_price()
            grand_total = subtotal - discount

            return JsonResponse({
                'success': True,
                'subtotal': float(subtotal),
                'discount': float(discount),
                'coupon_code': coupon_code,
                'grand_total': float(grand_total)
            })
        except KeyError as e:
            return JsonResponse({'success': False, 'error': f'Missing required data: {str(e)}'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': f'An unexpected error occurred: {str(e)}'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})
