from django import forms
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, Http404
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import redirect


from .models import Bid, Listing, User


class NewListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ["item", "description", "price",
                  "currency", "image_url", "category"]


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ["item", "bid"]
        widgets = {
            "item": forms.HiddenInput
        }


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
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


def listing(request, id=0):
    if request.method == "POST":
        form = NewListingForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.created_by = request.user
            obj.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        item = Listing.objects.get(id=id)
        bids = Bid.objects.filter(item=item)
        is_max_bid = bids and max(
            bids, key=lambda b: b.bid).bid_by.id == request.user.id
        return render(request, "auctions/listing.html", {
            "item": item,
            "total_bids": len(bids),
            "is_max_bid": is_max_bid,
            "bid_form": BidForm(None, initial={
                "item": item,
                "bid": 0,
            }),
        })


def create_listing(request):
    if request.method == "GET" and request.user.is_authenticated:
        return render(request, "auctions/create_listing.html", {
            "form": NewListingForm()
        })


def bid(request):
    if request.method == "POST":
        form = BidForm(request.POST)
        if form.is_valid():
            if bid.Bid > max("price", "is_max_bid"):
                obj = form.save(commit=False)
                obj.bid_by = request.user
                obj.save()
                return HttpResponseRedirect(reverse("index"))
            else:
                return HttpResponseNotFound("Page not found")
            
        