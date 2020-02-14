from custom_user.models import MyCustomUser
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from .forms import LoginForm


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
