from django.db import models

# Create your models here.
from customers.models import Customer
from products.models import Product


class orders(models.Model):
    owner=models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,related_name='orders')
    LIVE=1
    DELETE=0
    DELETE_choice=((LIVE,'live'),(DELETE,'delete'))
    CART_STAGE=0
    ORDER_CONFIRMED=1
    ORDER_PROCESSED=2
    ORDER_DELIVERED=3
    ORDER_REJECTED=4
    
    STATUS_CHOICE=((ORDER_CONFIRMED,'ORDER_CONFIRMED'),(ORDER_PROCESSED,'ORDER_PROCESSED'),(ORDER_DELIVERED,"ORDER_DELIVERED"),( ORDER_REJECTED," ORDER_REJECTED"))
    order_status=models.IntegerField(choices=STATUS_CHOICE,default=CART_STAGE)

    delete_status=models.IntegerField(choices=DELETE_choice,default=LIVE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)



class CartItem(models.Model):
    product=models.ForeignKey(Product,on_delete=models.SET_NULL,null=True,related_name="added_carts")
    quantity=models.PositiveIntegerField(default=1)
    owner=models.ForeignKey(orders,on_delete=models.CASCADE,related_name='added_items')
    
    @property
    def total_price(self):
        if self.product is None:
            return 0
        return self.product.price * self.quantity




class CheckoutDetails(models.Model):
    order = models.OneToOneField(orders, on_delete=models.CASCADE, related_name="checkout_details")

    fullname = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()
    pincode = models.CharField(max_length=10)
    payment_method = models.CharField(max_length=20)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.fullname} - Order {self.order.id}"

