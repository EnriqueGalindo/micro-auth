from custom_user.models import MyCustomUser
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from .forms import LoginForm, RegisterForm
from django.contrib.auth.decorators import login_required


@login_required()
def index_view(request):
    users = MyCustomUser.objects.all()
    return render(request, "index.html", {"users": users})


def login_view(request):
    html = "genericForm.html"

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(username=data["username"],
                                password=data["password"])
            if user:
                login(request, user)
                return redirect(request.GET.get("next", "/"))
            else:
                return HttpResponse("invalid authentication")

    form = LoginForm()

    return render(request, html, {'form': form})


def register_view(request):
    html = "genericForm.html"

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = MyCustomUser.objects.create_user(
                username=data["username"],
                password=data["password"]
            )
            login(request, user)
            return redirect(reverse("home"))

    form = RegisterForm()

    return render(request, html, {'form': form})