from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from customers.models import Customer

from .models import orders, CartItem,CheckoutDetails

from products.models import Product


import stripe
from django.conf import settings
from django.urls import reverse

stripe.api_key=settings.STRIPE_SECRET_KEY



@login_required
def cart_view(request):
# Safely get or create customer
    customer, created = Customer.objects.get_or_create(
        user=request.user,
        defaults={
            "name": request.user.username,
            "address": "",
            "phone": "0000000000"
        }
    )
 # Get current cart order
    order = orders.objects.filter(
        owner=customer,
        order_status=orders.CART_STAGE
    ).first()

    subtotal = 0
    if order:
        subtotal = sum(item.total_price for item in order.added_items.all())

    shipping = 50
    total = subtotal + shipping if subtotal > 0 else 0

    if subtotal>=500:
        shipping=0
        total = subtotal + shipping if subtotal > 0 else 0

    context = {
        "order": order,
        "subtotal": subtotal,
        "shipping": shipping,
        "total": total
    }

    return render(request, "cart.html", context)



@login_required
def update_cart(request, item_id):

    # Block direct URL access
    if request.method != "POST":
        return redirect("cart")

    item = get_object_or_404(
        CartItem,
        id=item_id,
        owner__owner__user=request.user
    )

    action = request.POST.get("action")

    if action == "increase":
        item.quantity += 1

    elif action == "decrease":
        if item.quantity > 1:
            item.quantity -= 1

    item.save()
    return redirect("cart")




@login_required
def remove_cart_item(request, item_id):
 # Only allow deleting own cart items
    item = get_object_or_404(
        CartItem,
        id=item_id,
        owner__owner__user=request.user
    )

    item.delete()
    return redirect("cart")



@login_required
def add_to_cart(request, product_id):
 # Get or create customer safely
    customer, _ = Customer.objects.get_or_create(
        user=request.user,
        defaults={
            "name": request.user.username,
            "address": "",
            "phone": "0000000000"
        }
    )

    # Get or create active cart
    order, _ = orders.objects.get_or_create(
        owner=customer,
        order_status=orders.CART_STAGE
    )

    # Get product
    product = get_object_or_404(Product, id=product_id)

    # Get or create cart item
    cart_item, created = CartItem.objects.get_or_create(
        owner=order,
        product=product
    )

    # If product already in cart, increase quantity
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect("cart")



@login_required
def checkout(request):
    customer = Customer.objects.get(user=request.user)

    # Get active cart order
    order = orders.objects.filter(
        owner=customer,
        order_status=orders.CART_STAGE
    ).first()

    if not order:
        return redirect("cart")

    # Calculate price
    subtotal = sum(item.total_price for item in order.added_items.all())
    shipping = 50
    if subtotal >= 500:
        shipping = 0

    total = subtotal + shipping

    if request.method == "POST":
        fullname = request.POST.get("fullname")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        address = request.POST.get("address")
        pincode = request.POST.get("pincode")
        payment_method = request.POST.get("payment_method")

        # 🔥 Prevent UNIQUE constraint error
        checkout_obj, created = CheckoutDetails.objects.get_or_create(
            order=order,
            defaults={
                "fullname": fullname,
                "phone": phone,
                "email": email,
                "address": address,
                "pincode": pincode,
                "payment_method": payment_method,
            }
        )

        # If exists, update fields
        if not created:
            checkout_obj.fullname = fullname
            checkout_obj.phone = phone
            checkout_obj.email = email
            checkout_obj.address = address
            checkout_obj.pincode = pincode
            checkout_obj.payment_method = payment_method
            checkout_obj.save()

        # ⚡ CARD → Redirect to Stripe
        if payment_method == "CARD":
            return redirect("stripe_pay", order_id=order.id)

        # COD / UPI → confirm order immediately
        order.order_status = orders.ORDER_CONFIRMED
        order.save()

        return redirect("success",order_id=order.id)

    return render(request, "checkout.html", {
        "order": order,
        "subtotal": subtotal,
        "shipping": shipping,
        "total": total
    })


 
      

def success(request, order_id):
    order = orders.objects.get(id=order_id)
    return render(request, "ordersuccess.html", {"order": order})




def stripe_pay(request, order_id):
    stripe.api_key = settings.STRIPE_SECRET_KEY

    # Get user's active order
    order = orders.objects.get(id=order_id, owner__user=request.user)

    # Calculate billing total
    subtotal = sum(item.total_price for item in order.added_items.all())
    shipping = 0 if subtotal >= 500 else 50
    total_amount = int((subtotal + shipping) * 100)  # INR paise

    # Create Stripe Checkout Session
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],   # ✅ ENABLE UPI
        line_items=[
            {
                'price_data': {
                    'currency': 'inr',
                    'product_data': {'name': f"Order #{order.id}"},
                    'unit_amount': total_amount,
                },
                'quantity': 1,
            }
        ],
        mode='payment',

        # Redirect after success
        success_url=request.build_absolute_uri(
            reverse("stripe_success", args=[order.id])
        ),

        # Redirect if cancelled
        cancel_url=request.build_absolute_uri(reverse("checkout")),
    )

    return redirect(session.url)








def stripe_success(request, order_id):
    order = orders.objects.get(id=order_id, owner__user=request.user)
    order.order_status = orders.ORDER_CONFIRMED
    order.save()
    return redirect("success",order_id=order.id)



@login_required
def track_order(request, order_id):
    order = get_object_or_404(orders, id=order_id, owner__user=request.user)

    status_map = {
        orders.CART_STAGE: "Order Placed",
        orders.ORDER_CONFIRMED: "Order Confirmed",
        orders.ORDER_PROCESSED: "Order Processed",
        orders.ORDER_DELIVERED: "Delivered",
        orders.ORDER_REJECTED: "Order Rejected",
    }

    current_status = status_map.get(order.order_status, "Unknown")

    return render(request, "track_order.html", {
        "order": order,
        "current_status": current_status,
        "status_map": status_map,
    })



@login_required
def my_orders(request):
    customer = Customer.objects.get(user=request.user)
    all_orders = orders.objects.filter(owner=customer).order_by('-id')

    # Attach totals inside each order
    for order in all_orders:
        order.total_amount = sum(item.total_price for item in order.added_items.all())

    return render(request, "my_orders.html", {
        "all_orders": all_orders
    })



