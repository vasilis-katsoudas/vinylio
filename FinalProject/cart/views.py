from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from cart.models import CartItem
from home.models import Vinyl
from django.db.models import Q
from django.contrib import messages

def add_to_cart(request, vinyl_id):
    if not request.user.is_authenticated:
        messages.warning(request, "You must login to perform this action.")
        return redirect('login')
    vinyl = get_object_or_404(Vinyl, id=vinyl_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, vinyl=vinyl)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, f"{vinyl.title} added to cart successfully.")
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    messages.info(request, f"{item.vinyl.title} removed from cart.")
    return redirect('cart')

def cart(request):
    if not request.user.is_authenticated:
        messages.warning(request, "You must login to perform this action.")
        return redirect('login')
    items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.vinyl.price * item.quantity for item in items)
    for item in items:
        item.subtotal = item.vinyl.price * item.quantity
    return render(request, 'cart/cart.html', {'cart_items': items, 'total_price': total_price})