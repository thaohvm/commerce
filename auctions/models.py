from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return f"{self.username} - {self.email}"


class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Listing(models.Model):
    item = models.CharField(max_length=64)
    price = models.FloatField()
    currency = models.CharField(max_length=3)
    image = models.ImageField(upload_to="uploads/images", blank=True)
    description = models.CharField(max_length=64, blank=True)
    categories = models.ForeignKey(Category, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return (
            f"{self.item} : {self.description} - "
            f"{self.price}{self.currency} - {self.created}"
        )

# class Bids(models.Model):
#     item = models.CharField(max_length=64)
#     bid_th = models.IntegerField()
#     bid = models.IntegerField()

#     def __str__(self):
#         return f"{self.item} : {self.bid_th} ({self.bid})"


# class Comments(models.Model):
#     user = models.CharField(max_length=64)
#     content = models.IntegerField()

#     def __str__(self):
#         return f"{self.item} : {self.bid_th} ({self.bid})"
