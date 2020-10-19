from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing", views.listing, name="listing"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("listing/create", views.create_listing, name="create_listing"),
    path("listing/close/<int:id>", views.close_listing, name="close_listing"),
    path("bid", views.bid, name="bid"),
    path("comment", views.comment, name="comment"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("category", views.category, name="category"),
    path("category/<int:id>", views.category, name="category"),
]
