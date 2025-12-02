from django.contrib import admin

# Register your models here.


from django.contrib import admin
from .models import orders
from .models import CartItem
from .models import CheckoutDetails


admin.site.register(orders)

admin.site.register(CartItem)

admin.site.register(CheckoutDetails)


