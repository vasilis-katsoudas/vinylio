"""
URL configuration for FinalProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from home import views
from cart import views as cart_views
from wishlist import views as wishlist_views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('register/', include('register.urls')),
    path('', include("django.contrib.auth.urls")),
    path('category/<int:category_id>/', views.category, name='category'),
    path('vinyl/<int:pk>/', views.vinyl_detail, name='vinyl_detail'),
    path('live-search/', views.live_search, name='live_search'),
    path('search/', views.search_results, name='search_results'),
    path('wishlist/', wishlist_views.wishlist, name='wishlist'),
    path('cart/', cart_views.cart, name='cart'),
    path('wishlist/add/<int:vinyl_id>/', wishlist_views.add_to_wishlist, name='add_to_wishlist'),
    path('cart/add/<int:vinyl_id>/', cart_views.add_to_cart, name='add_to_cart'),
    path('wishlist/remove/<int:item_id>/', wishlist_views.remove_from_wishlist, name='remove_from_wishlist'),
    path('cart/remove/<int:item_id>/', cart_views.remove_from_cart, name='remove_from_cart'),
    path('profile/', views.profile, name='profile'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('genre/<str:genre>/', views.genre_vinyls, name='genre'),
    path('rate/<int:vinyl_id>/', views.rate_vinyl, name='rate'),
    path('favorite/<int:vinyl_id>/', views.toggle_favorite, name='favorite'),
    path('favorites/', views.favorites, name='favorites')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
