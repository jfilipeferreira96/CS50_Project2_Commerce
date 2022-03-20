from django.contrib import admin
from .models import Category, User, Auction, Comment, Watchlist, Bid
# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title")


class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "password")


class AuctionAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "seller", "created_at")


class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "auction_id", "user", "comment", "timestamp")


class WatchlistAdmin(admin.ModelAdmin):
    list_display = ("id", "user_id", "auctions_id")


class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "amount", "user", "auction")


admin.site.register(Category, CategoryAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Auction, AuctionAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Watchlist, WatchlistAdmin)
admin.site.register(Bid, BidAdmin)
