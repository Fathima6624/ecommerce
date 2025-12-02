from django.urls import path

from . import views

urlpatterns = [
    path("cart/",views.cart_view,name="cart"),
    path("updatecart/<int:item_id>/",views.update_cart,name="updatecart"),
    path("removeitem/<int:item_id>/",views.remove_cart_item,name="removeitem"),
    path("addtocart/<int:product_id>/",views.add_to_cart,name="addtocart"),
    path("checkout/",views.checkout,name="checkout"),
    path("success//<int:order_id>/",views.success,name="success"),
    path("stripe/pay/<int:order_id>/", views.stripe_pay, name="stripe_pay"),
path("stripe/success/<int:order_id>/", views.stripe_success, name="stripe_success"),
path("track/<int:order_id>/", views.track_order, name="track_order"),
path("my_orders/", views.my_orders, name="my_orders"),




    
]