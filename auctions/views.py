from email.mime import image
from queue import Empty
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from .models import Category, User,Listing


def index(request):
    return render(request, "auctions/index.html",{
        "listings": Listing.objects.all(),
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def add_listing(request):
    if request.method == 'POST':
        title = request.POST['title']
        image_url = request.POST['image_url']
        description = request.POST['description']
        price = request.POST['price']
        category = request.POST['category']
        if title == "" or image_url  == "" or description == "" or price == "":
            return render(request, "auctions/add_listing.html",{
                "message":"Fields cannot be empty"
            })
        else: 
            listing = Listing.objects.create(title=title,description=description,starting_bid=price,image_url=image_url,category=Category.objects.get(name=category))
            listing.save()
            return redirect(reverse('index'))
        
    return render(request, "auctions/add_listing.html",{
        "categories":Category.objects.all()
    })
