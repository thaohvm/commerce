from django import forms
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, HttpResponseBadRequest
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import redirect


from .models import Bid, Comment, Listing, User, Watchlist, Category


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


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["item", "content"]
        widgets = {
            "item": forms.HiddenInput
        }


class WatchlistForm(forms.ModelForm):
    delete = forms.BooleanField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Watchlist
        fields = ["item"]
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
        is_max_bid = request.user.id is not None and bids and max(
            bids, key=lambda b: b.bid).bid_by.id == request.user.id
        max_bid_user = max(bids, key=lambda b: b.bid).bid_by if bids else None
        comments = Comment.objects.filter(item=item)
        watchlisted = request.user.is_authenticated and Watchlist.objects.filter(
            item=item, user=request.user).count() > 0

        return render(request, "auctions/listing.html", {
            "item": item,
            "price": max(bids, key=lambda b: b.bid).bid if bids else item.price,
            "total_bids": len(bids),
            "is_max_bid": is_max_bid,
            "max_bid_user": max_bid_user,
            "watchlisted": watchlisted,
            "watchlist_form": WatchlistForm(None, initial={
                "item": item,
                "delete": watchlisted,
            }),
            "bid_form": BidForm(None, initial={
                "item": item,
                "bid": 0,
            }),
            "comments": sorted(comments, key=lambda c: c.created, reverse=True),
            "comment_form": CommentForm(None, initial={
                "item": item,
                "content": "",
            }),
        })


def create_listing(request):
    if request.method == "GET" and request.user.is_authenticated:
        return render(request, "auctions/create_listing.html", {
            "form": NewListingForm()
        })


def close_listing(request, id):
    if request.method == "POST":
        listing = Listing.objects.get(id=id)
        if request.user == listing.created_by:
            listing.closed = True
            listing.save()
            return HttpResponseRedirect(reverse("listing", args=[id]))
    return HttpResponseBadRequest("Invalid request!")


def bid(request):
    if request.method == "POST":
        form = BidForm(request.POST)
        if form.is_valid():
            item = form.cleaned_data["item"]
            bid = form.cleaned_data["bid"]
            bids = Bid.objects.filter(item=item)
            max_bid = max(bids, key=lambda b: b.bid).bid if bids else item.price
            if bid > max_bid:
                obj = form.save(commit=False)
                obj.bid_by = request.user
                obj.save()
                return HttpResponseRedirect(reverse("listing", args=[item.id]))

        return HttpResponseBadRequest("Invalid bid!")


def comment(request):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.created_by = request.user
            obj.save()
            return HttpResponseRedirect(reverse("listing", args=[form.cleaned_data["item"].id]))

        return HttpResponseBadRequest("Invalid comment!")


def watchlist(request):
    if request.method == "POST":
        form = WatchlistForm(request.POST)
        if form.is_valid():
            if form.cleaned_data["delete"]:
                Watchlist.objects.filter(
                    item=form.cleaned_data["item"], user=request.user).delete()
            else:
                obj = form.save(commit=False)
                obj.user = request.user
                obj.save()
            return HttpResponseRedirect(reverse("listing", args=[form.cleaned_data["item"].id]))
    else:
        watchlist = Watchlist.objects.filter(user=request.user)
        return render(request, "auctions/watchlist.html", {
            "watchlist": watchlist
        })


def category(request, id=0):
    if id > 0:
        category = Category.objects.get(id=id)
        listings = Listing.objects.filter(category=id)
        return render(request, 'auctions/category.html', {
            "category": category,
            "listings": listings
        })
    else:
        categories = Category.objects.all()
        return render(request, 'auctions/categories.html', {
            "categories": categories
        })
