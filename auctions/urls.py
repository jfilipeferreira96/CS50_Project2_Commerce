from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:title>",  views.category, name="categories"),
    path("auction/<int:auction_id>", views.product_page, name="auction"),
    path("create_auction", views.create, name="create"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("comment/<int:auction_id>", views.comment, name="comment"),
    path("bid/<int:auction_id>", views.bid, name="bid"),
    path("close/<int:auction_id>", views.closebid, name="closebid"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
