from django.shortcuts import render
from django.http import HttpResponse
from .models import Vinyl

# Create your views here.
def home(request):
    vinyls = Vinyl.objects.all() 
    return render(request, 'home/welcome.html', {'vinyls': vinyls})

def add_to_wishlist(request, vinyl_id):
    vinyl = get_object_or_404(Vinyl, id=vinyl_id)
    Wishlist.objects.get_or_create(user=request.user, vinyl=vinyl)
    return redirect('home')