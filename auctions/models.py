from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

    def __str__(self):
        return f"{self.username} ({self.id})"


class Category(models.Model):
    title = models.CharField(max_length=32, blank=False)
    image_url = models.URLField(blank=True)

    def __str__(self):
        return f"{self.title}"


class Auction(models.Model):
    seller = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="seller")
    title = models.CharField(max_length=64, blank=False)
    description = models.TextField(max_length=264, blank=False)
    image_url = models.URLField(blank=True)
    category = models.ForeignKey(
        Category,
        blank=False,
        on_delete=models.CASCADE
    )
    starting_bid = models.DecimalField(
        max_digits=7, decimal_places=2, default=0.0)
    current_bid = models.DecimalField(
        max_digits=7, decimal_places=2, default=0.0)
    current_bid_user = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True,
        null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Auction {self.id}: {self.title} - Seller {self.seller} - timestamp: {self.created_at}"


class Comment(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user")
    comment = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment {self.id} on auction {self.auction.id} made by {self.user.username} at {self.timestamp} - {self.comment}"


class Watchlist(models.Model):

    auctions = models.ForeignKey(
        Auction, blank=False, on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="watchlist")

    def __str__(self):
        return f"User {self.user} is watching {self.auctions}"


class Bid(models.Model):
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    auction = models.ForeignKey(
        Auction, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bid {self.id}: {self.amount} on {self.auction.title} by {self.user.username}"
