from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from .models import Vinyl, Category
from django.contrib.auth.decorators import login_required
from wishlist.models import Wishlist
from cart.models import CartItem
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import logout
from django.contrib.auth.models import User

def category(request, category_id):
    category = Category.objects.get(id=category_id)
    vinyls = Vinyl.objects.filter(categories=category)
    return render(request, 'home/category.html', {'category': category, 'vinyls': vinyls})

def home(request):
    query = request.GET.get('q')
    vinyls = Vinyl.objects.all()
    if query:
        vinyls = vinyls.filter(title__icontains=query)

    categories = Category.objects.all()
    category_vinyls = {cat: Vinyl.objects.filter(categories=cat)[:8] for cat in categories}

    return render(request, 'home/home.html', {
        'categories': categories,
        'category_vinyls': category_vinyls,
        'vinyls': vinyls
    })

def vinyl_detail(request, pk):
    vinyl = get_object_or_404(Vinyl, pk=pk)
    return render(request, 'home/vinyl_detail.html', {'vinyl': vinyl})

def live_search(request):
    query = request.GET.get('q', '')
    vinyls = Vinyl.objects.filter(
        Q(title__icontains=query) | Q(artist__icontains=query)
    )[:5]
    data = {
        'results': [
            {
                'id': v.id,
                'title': v.title,
                'artist': v.artist,
                'image': v.image.url if v.image else ''
            }
            for v in vinyls
        ]
    }
    return JsonResponse(data)

def search_results(request):
    query = request.GET.get('q')
    vinyls = Vinyl.objects.none()

    if query:
        vinyls = Vinyl.objects.filter(
            Q(title__icontains=query) | Q(artist__icontains=query)
        )

    return render(request, 'home/search_results.html', {
        'query': query,
        'vinyls': vinyls
    })

@login_required
def profile(request):
    user_form = CustomUserChangeForm(request.POST or None, instance=request.user)
    password_form = PasswordChangeForm(request.user, request.POST or None)

    if request.method == 'POST':
        if 'save_profile' in request.POST:
            if user_form.is_valid():
                cleaned = user_form.cleaned_data
                if not cleaned['first_name'] or not cleaned['last_name'] or not cleaned['email']:
                    messages.error(request, "All fields are required.")
                else:
                    user_form.save()
                    messages.success(request, "Profile updated successfully.")
                    return redirect('profile')

        elif 'change_password' in request.POST and password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Password changed successfully.")
            return redirect('profile')

    return render(request, 'home/profile.html', {
        'form': user_form,
        'password_form': password_form
    })

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'password' in self.fields:
            del self.fields['password']
