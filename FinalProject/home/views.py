from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Vinyl, Category

def add_to_wishlist(request, vinyl_id):
    vinyl = get_object_or_404(Vinyl, id=vinyl_id)
    Wishlist.objects.get_or_create(user=request.user, vinyl=vinyl)
    return redirect('home')

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

def add_to_cart(request, vinyl_id):
    #TODO
    return HttpResponseRedirect(reverse('vinyl_detail', args=[vinyl_id]))

def add_to_wishlist(request, vinyl_id):
    #TODO
    return HttpResponseRedirect(reverse('vinyl_detail', args=[vinyl_id]))