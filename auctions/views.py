from genericpath import exists
from webbrowser import get
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import datetime

from .models import Category, User, Auction, Comment, Watchlist, Bid


def index(request):
    # Active Listings
    active_auctions = Auction.objects.filter(
        active=True).order_by("-created_at")
    if request.user.id is None:
        return render(request, "auctions/index.html", {
            "active_auctions": active_auctions,
            "watchlist": 'none',
            "title": 'Active Listings'
        })
    else:
        user_watchlist = Watchlist.objects.filter(
            user_id=request.user.id)

        watchlist_ids = []
        if len(user_watchlist) > 0:
            for item in user_watchlist:
                watchlist_ids.append(item.auctions_id)

        return render(request, "auctions/index.html", {
            "active_auctions": active_auctions,
            "watchlist": watchlist_ids,
            "user_id": request.user.id,
            "title": 'Active Listings'
        })

# renders every single category


def categories(request, title=None):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all()
    })

# redirects to a spefic category


def category(request, title):

    if title is not None:
        category_pk = Category.objects.get(title=title).pk

        if Category.objects.get(title=title):
            active_auctions = Auction.objects.filter(active=True,
                                                     category=category_pk).order_by("-created_at")
            # watchlist button handling
            user_watchlist = Watchlist.objects.filter(
                user_id=request.user.id)
            watchlist_ids = []
            if len(user_watchlist) > 0:
                for item in user_watchlist:
                    watchlist_ids.append(item.auctions_id)

            return render(request, "auctions/index.html", {
                "active_auctions": active_auctions,
                "watchlist": watchlist_ids,
                "user_id": request.user.id,
                "title": title
            })
    else:
        return render(request, "auctions/404.html", {
            "message": 'Invalid Category'
        })

    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all()
    })


def product_page(request, auction_id):
    # get the comments
    comments = Comment.objects.select_related(
        'user').filter(auction_id=auction_id).order_by("timestamp").reverse()

    # if the product page that we are visiting is on watchlist then watchlist value equals to 1, else 0
    if request.user.id is None:
        return render(request, "auctions/product_page.html", {
            "product": Auction.objects.get(pk=auction_id),
            "comments": comments,
            "watchlist": 0
        })
    else:
        user_watchlist = Watchlist.objects.filter(
            user_id=request.user.id, auctions_id=auction_id)

        watchlist = 0
        if len(user_watchlist) > 0:
            watchlist = 1

        return render(request, "auctions/product_page.html", {
            "product": Auction.objects.get(pk=auction_id),
            "comments": comments,
            "user_id": request.user.id,
            "watchlist": watchlist
        })


def watchlist(request):
    if request.user.id is None:
        return HttpResponseRedirect(reverse("login"))
    else:
        # Handling add/remove to wishlist
        if request.method == "POST":
            # Info about the auction
            auction_id = request.POST.get("auction_id")
            info = request.POST.get("info")
            if info == 'add':
                add_to_watchlist = Watchlist(
                    auctions=Auction.objects.get(pk=auction_id), user=User.objects.get(pk=request.user.id))
                add_to_watchlist.save()
                return redirect(f"watchlist")
            else:
                del_watchlist_item = Watchlist.objects.filter(
                    auctions=Auction.objects.get(pk=auction_id), user=User.objects.get(pk=request.user.id))
                del_watchlist_item.delete()
                return redirect(f"watchlist")

        # Rendering watchlist page
        else:
            user_watchlist = Watchlist.objects.filter(
                user_id=request.user.id)

            watchlist_items = []

            if len(user_watchlist) > 0:
                for item in user_watchlist:
                    watchlist_items.append(
                        Auction.objects.get(pk=item.auctions_id))

                return render(request, "auctions/index.html", {
                    "active_auctions": watchlist_items,
                    "title": 'Watchlist'
                })
            else:  # watchlist is empty
                return render(request, "auctions/index.html", {
                    "active_auctions": watchlist_items,
                    "title": 'Empty Watchlist'
                })


@ login_required(login_url="/login")
def create(request):
    # Form handling
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        image_url = request.POST["image_url"]
        starting_price = request.POST["starting_price"]
        category_id = request.POST["category_select"]

        # Double check if the user is trully logged in
        if request.user.id is None:
            return HttpResponseRedirect(reverse("login"))
        else:
            # insert in the db
            auction = Auction(
                seller=User.objects.get(pk=request.user.id),
                title=title,
                description=description,
                image_url=image_url,
                created_at=datetime.datetime.now(),
                starting_bid=starting_price,
                active=True,
                category=Category.objects.get(pk=category_id)
            )
            auction.save()
            # if its successfull
            return redirect(f"categories/{Category.objects.get(pk=category_id).title}")

    return render(request, "auctions/create_auction.html", {
        "categories": Category.objects.all()
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
                "message": "Invalid username or password."
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
                "message": "Passwords must match.",
                "alert": "Password"
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken.",
                "alert": "Username"
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required(login_url="/login")
def comment(request, auction_id):
    if request.method == 'POST':

        comment = request.POST['comment_area']
        add_comment = Comment(
            auction=Auction.objects.get(pk=auction_id),
            user=User.objects.get(pk=request.user.id),
            comment=comment
        )
        add_comment.save()
        # returns the same page
        return HttpResponseRedirect(reverse("auction", args=(auction_id,)))
    else:
        return render(request, "auctions/index.html")


@login_required(login_url="/login")
def bid(request, auction_id):
    if request.method == 'POST':
        bid_price = request.POST['bid_input']
        # queries
        auction = Auction.objects.select_related(
            'seller').get(pk=auction_id)
        comments = Comment.objects.select_related(
            'user').filter(auction_id=auction_id).order_by("timestamp").reverse()
        user_watchlist = Watchlist.objects.filter(
            user_id=request.user.id, auctions_id=auction_id)
        watchlist = 0
        if len(user_watchlist) > 0:
            watchlist = 1

        if auction.seller_id == request.user.id:
            # error message - seller cannot bid on his own listing
            return render(request, "auctions/product_page.html", {
                "product": Auction.objects.get(pk=auction_id),
                "comments": comments,
                "watchlist": watchlist,
                "error": 'Seller cannot bid on his own listing.'
            })

        if float(bid_price) >= auction.starting_bid and float(bid_price) > auction.current_bid:
            # insert in both tables:
            # 1 - bid table
            bid = Bid(
                amount=float(bid_price),
                auction=Auction.objects.get(pk=auction_id),
                user=User.objects.get(pk=request.user.id)
            )
            bid.save()
            # 2 - Updates the current bid in the auction table
            current_bid_update = Auction.objects.get(pk=auction_id)
            current_bid_update.current_bid = float(bid_price)
            current_bid_update.current_bid_user = User.objects.get(
                pk=request.user.id)
            current_bid_update.save()

            # Renders the product page
            return render(request, "auctions/product_page.html", {
                "product": Auction.objects.get(pk=auction_id),
                "comments": comments,
                "watchlist": watchlist,
                "user_id": request.user.id,
                "success": 'success'
            })
        else:
            # displaying error message
            return render(request, "auctions/product_page.html", {
                "product": Auction.objects.get(pk=auction_id),
                "comments": comments,
                "watchlist": watchlist,
                "user_id": request.user.id,
                "error": 'Your bid must be higher.'
            })

    else:
        return render(request, "auctions/index.html")


@login_required(login_url="/login")
def closebid(request, auction_id):
    if request.method == "POST":
        print(auction_id)
        close = Auction.objects.get(pk=auction_id)
        close.active = False
        close.save()
        if request.POST.get("info") == 'index':
            # returns the index page
            return HttpResponseRedirect(reverse("index"))

        else:
            # returns the product page
            return HttpResponseRedirect(reverse("auction", args=(auction_id,)))
