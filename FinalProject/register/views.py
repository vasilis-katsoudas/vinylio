from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterForm


# Create your views here.
def register(response):
    form = UserCreationForm()

    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
        return redirect("index")
    else:
        form = RegisterForm()

    return render(response, "register/register.html",{"form":form})
