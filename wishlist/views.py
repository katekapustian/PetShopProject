from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import WishlistItem
from shop.models import Product


@login_required
def wishlist_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    wishlist_item, created = WishlistItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        wishlist_item.quantity += quantity
    wishlist_item.save()
    return redirect('wishlist:wishlist_detail')


@login_required
def wishlist_remove(request, item_id):
    wishlist_item = get_object_or_404(WishlistItem, id=item_id, user=request.user)
    wishlist_item.delete()
    return redirect('wishlist:wishlist_detail')


@login_required
def wishlist_detail(request):
    wishlist_items = WishlistItem.objects.filter(user=request.user)
    return render(request, 'wishlist/wishlist.html', {'wishlist_items': wishlist_items})
