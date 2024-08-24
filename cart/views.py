from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from shop.models import Product, NewsletterSubscription
from .cart import Cart
from django.http import JsonResponse
from django.contrib import messages


def cart_detail(request):
    cart = Cart(request)
    email = request.user.email if request.user.is_authenticated else request.session.get('guest_email')

    discount, coupon_code = cart.get_discount(email)
    grand_total = cart.get_total_price_after_discount(email)

    if request.method == 'POST':
        coupon_input = request.POST.get('coupon_code')
        if coupon_input:
            try:
                subscription = NewsletterSubscription.objects.get(coupon_code=coupon_input, coupon_used=False)
                if subscription.email == email or not request.user.is_authenticated:
                    discount, coupon_code = cart.apply_coupon(subscription.email)
                    grand_total = cart.get_total_price_after_discount(subscription.email)
                    messages.success(request, "Coupon applied successfully!")
                else:
                    messages.error(request, "Invalid coupon code.")
            except NewsletterSubscription.DoesNotExist:
                messages.error(request, "Invalid or already used coupon code.")

    return render(request, 'cart/cart.html', {
        'cart': cart,
        'discount': discount,
        'coupon_code': coupon_code,
        'grand_total': grand_total
    })


def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', request.GET.get('quantity', 1)))
    cart.add(product=product, quantity=quantity, update_quantity=True)
    return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect('cart:cart_detail')


def cart_update(request):
    cart = Cart(request)
    if request.method == 'POST':
        for key, value in request.POST.items():
            if key.startswith('quantity_'):
                product_id = key.split('_')[1]
                product = get_object_or_404(Product, id=product_id)
                quantity = int(value)
                cart.add(product=product, quantity=quantity, update_quantity=True)
    return redirect('cart:cart_detail')


def cart_remove_ajax(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
        return JsonResponse({
            'success': True,
            'total_price': cart.get_total_price(),
            'cart_count': len(cart)
        })
    return JsonResponse({'success': False}, status=400)
