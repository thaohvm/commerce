from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return f"{self.username} - {self.email}"


class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"


class Listing(models.Model):
    item = models.CharField(max_length=64)
    price = models.FloatField()
    currency = models.CharField(max_length=3)
    image = models.ImageField(upload_to="uploads/images", blank=True)
    image_url = models.URLField(blank=True)
    description = models.TextField(max_length=256, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    closed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return (
            f"{self.item} : "
            f"{self.currency}{self.price} created by {self.created_by}"
        )


class Bid(models.Model):
    item = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bid = models.FloatField()
    bid_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.item} : {self.bid} ({self.bid_by})"


class Comment(models.Model):
    item = models.ForeignKey(Listing, on_delete=models.CASCADE)
    content = models.CharField(max_length=256)
    created = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.item} : {self.created} ({self.created_by}) says: ({self.content})"


class Watchlist(models.Model):
    item = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} : {self.item}"
