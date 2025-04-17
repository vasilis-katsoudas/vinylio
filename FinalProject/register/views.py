from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import RegisterForm

# Create your views here.
def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.email = form.cleaned_data.get('email')
            user.save()

            login(response, user)
            messages.success(response, "Account created successfully.")
            return redirect("home")
    else:
        form = RegisterForm()

    return render(response, "register/register.html", {"form": form})
