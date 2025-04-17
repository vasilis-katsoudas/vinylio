from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from wishlist.models import Wishlist
from home.models import Vinyl
from django.db.models import Q
from django.contrib import messages
from cart.models import CartItem

def add_to_wishlist(request, vinyl_id):
    if not request.user.is_authenticated:
        messages.warning(request, "You must login to perform this action.")
        return redirect('login')
    vinyl = get_object_or_404(Vinyl, id=vinyl_id)
    Wishlist.objects.get_or_create(user=request.user, vinyl=vinyl)
    messages.success(request, f"{vinyl.title} added to wishlist successfully.")
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def remove_from_wishlist(request, item_id):
    item = get_object_or_404(Wishlist, id=item_id, user=request.user)
    item.delete()
    messages.info(request, f"{item.vinyl.title} removed from wishlist.")
    return redirect('wishlist')

def wishlist(request):
    if not request.user.is_authenticated:
        messages.warning(request, "You must login to perform this action.")
        return redirect('login')
    items = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist/wishlist.html', {'wishlist_items': items})