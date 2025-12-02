from django.shortcuts import render, redirect
from .forms import RegistrationForm, CustomLoginForm
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, "index.html")


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully!")
            return redirect("login")

    else:
        form = RegistrationForm()

    return render(request, "account.html", {"form": form})


def loginform(request):
    if request.method == "POST":
        form = CustomLoginForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Login successful")
            return redirect("index")

    else:
        form = CustomLoginForm()

    return render(request, "loginform.html", {"form": form})



# logout
@login_required
def log_out(request):
    logout(request)
    return redirect("login")