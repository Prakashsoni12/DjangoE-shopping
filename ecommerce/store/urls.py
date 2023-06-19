from django.urls import path
from . import views
from store.controller import authview, cart, wishlist, checkout, order

urlpatterns = [
    path('', views.home, name='home'),
    path('collections', views.collections, name='collections'),
    path('collections/<str:slug>', views.collectionsview, name='collectionsview'),
    path('collections/<str:cate_slug>/<str:prod_slug>',
         views.productview, name='productview'),
    path("product-list", views.productlistajax),
    path("searchproducts", views.searchproducts, name="searchproducts"),
    path("ragister", authview.ragister, name="ragister"),
    path("login/", authview.loginpage, name="loginpage"),
    path("logout/", authview.logoutpage, name='logoutpage'),
    path('add-to-cart', cart.addtocart, name='addtocart'),
    path("cart/", cart.viewcart, name="viewcart"),
    path("update-cart", cart.updatecart, name='updatecart'),
    path("delete-cart-item", cart.deletecartitem, name="deletecartitem",),
    path("wishlisht", wishlist.index, name="wishlist"),
    path("add-to-wishlist", wishlist.addtowishlist, name="addtowishlist"),
    path("delete-wishlist-item", wishlist.deletewishlistitem,
         name="deletewishlistitem"),
    path("checkout", checkout.index, name="checkout"),
    path("place-order", checkout.placeorder, name="placeorder"),
    path("proceed-to-pay", checkout.razorpaycheck),
    path("my-orders", order.index, name="my-orders"),
    path('view-orders/<str:t_no>', order.view, name="orderview"),
]
