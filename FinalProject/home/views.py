from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from .models import Vinyl, Category, Favorite, Rating, ViewHistory
from django.contrib.auth.decorators import login_required
from wishlist.models import Wishlist
from cart.models import CartItem
from django.db.models import Q, Count, IntegerField, Case, When
from django.contrib import messages
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.db.models.functions import Lower

GENRE_LABELS = dict(Vinyl.GENRE_CHOICES)

def category(request, category_id):
    category = Category.objects.get(id=category_id)
    vinyls = Vinyl.objects.filter(categories=category)
    return render(request, 'home/category.html', {'category': category, 'vinyls': vinyls})

def home(request):
    sort = request.GET.get('sort')
    query = request.GET.get('q')
    vinyls = Vinyl.objects.all()
    if query:
        vinyls = vinyls.filter(title__icontains=query)

    if sort == 'title':
        vinyls = vinyls.order_by(Lower('title'))
    elif sort == 'year':
        vinyls = vinyls.order_by('-release_date')
    elif sort == 'likes':
        vinyls = vinyls.annotate(like_count=Count('favorites')).order_by('-like_count')

    categories = Category.objects.all()
    category_vinyls = {cat: Vinyl.objects.filter(categories=cat)[:8] for cat in categories}

    history = []
    if request.user.is_authenticated:
        history = ViewHistory.objects.filter(user=request.user).select_related('vinyl')[:8]
    
    genres = Vinyl.GENRE_CHOICES
    most_liked = Vinyl.objects.annotate(like_count=Count('favorites')).order_by('-like_count')[:8]

    return render(request, 'home/home.html', {
        'categories': categories,
        'category_vinyls': category_vinyls,
        'vinyls': vinyls,
        'genres': genres,
        'most_liked': most_liked,
        'history': history
    })

def vinyl_detail(request, pk):
    vinyl = get_object_or_404(Vinyl, pk=pk)

    #filter vinyls to show in recommended based on priority
    recommended_vinyls = Vinyl.objects.filter(
        Q(artist=vinyl.artist) |
        Q(genre=vinyl.genre) |
        Q(categories__in=vinyl.categories.all())
    ).exclude(pk=vinyl.pk).distinct().annotate(
        priority=Case(
            When(artist=vinyl.artist, then=0),
            When(genre=vinyl.genre, then=1),
            default=2,
            output_field=IntegerField()
        )
    ).order_by('priority')[:5]

    is_favorited = False
    average_rating = 0
    total_ratings = 0
    user_rating = 0

    if request.user.is_authenticated:
        is_favorited = vinyl.favorites.filter(user=request.user).exists()
        user_rating_obj = vinyl.ratings.filter(user=request.user).first()
        if user_rating_obj:
            user_rating = user_rating_obj.stars

    total_favorites = vinyl.favorites.count()

    ratings = vinyl.ratings.all()
    total_ratings = ratings.count()
    if total_ratings > 0:
        average_rating = sum(r.stars for r in ratings) / total_ratings

    if request.user.is_authenticated:
        ViewHistory.objects.update_or_create(user=request.user, vinyl=vinyl)

    return render(request, 'home/vinyl_detail.html', {
        'vinyl': vinyl,
        'recommended_vinyls': recommended_vinyls,
        'is_favorited': is_favorited,
        'total_favorites': total_favorites,
        'average_rating': average_rating,
        'total_ratings': total_ratings,
        'user_rating': user_rating
    })

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
        'vinyls': vinyls,
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

@login_required
def toggle_favorite(request, vinyl_id):
    vinyl = get_object_or_404(Vinyl, id=vinyl_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, vinyl=vinyl)
    if not created:
        favorite.delete()
        favorited = False
    else:
        favorited = True
    total = vinyl.favorites.count()
    return JsonResponse({'favorited': favorited, 'total': total})

@login_required
def rate_vinyl(request, vinyl_id):
    stars = int(request.POST.get("stars"))
    rating, created = Rating.objects.update_or_create(
        user=request.user,
        vinyl_id=vinyl_id,
        defaults={"stars": stars}
    )
    vinyl = Vinyl.objects.get(pk=vinyl_id)
    all_ratings = vinyl.ratings.all()
    total = all_ratings.count()
    avg = sum(r.stars for r in all_ratings) / total if total > 0 else 0
    return JsonResponse({'status': 'ok', 'rated': True, 'average': round(avg, 1), 'total': total})

def vinyls_sorted(request):
    sort = request.GET.get('sort', 'title')
    sort_map = {
        'title': 'title',
        'year': 'year_released',
        'likes': '-favorite_count'
    }
    vinyls = Vinyl.objects.annotate(favorite_count=Count('favorites')).order_by(sort_map.get(sort, 'title'))
    return render(request, 'home/all_vinyls.html', {'vinyls': vinyls})

def genre_vinyls(request, genre):
    sort = request.GET.get('sort')
    vinyls = Vinyl.objects.filter(genre=genre)

    if sort == 'title':
        vinyls = vinyls.order_by(Lower('title'))
    elif sort == 'year':
        vinyls = vinyls.order_by('-release_date')
    elif sort == 'likes':
        vinyls = vinyls.annotate(like_count=Count('favorites')).order_by('-like_count')

    genre_label = GENRE_LABELS.get(genre, genre)

    return render(request, 'home/genre_vinyls.html', {
        'genre': genre,
        'genre_label': genre_label,
        'vinyls': vinyls
    })

def favorites(request):
    liked_vinyls = Vinyl.objects.filter(favorites__user=request.user)
    return render(request, 'home/favorites.html', {
        'liked_vinyls': liked_vinyls
    })
