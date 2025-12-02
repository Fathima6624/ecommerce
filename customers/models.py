from django.db import models

# Create your models here.

from django.contrib.auth.models import User



class Customer(models.Model):
    LIVE=1
    DELETE=0
    DELETE_choice=((LIVE,'live'),(DELETE,'delete'))
    name=models.CharField(max_length=200)
    address=models.TextField()
    phone=models.CharField(max_length=10)
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="customer")
    delete_status=models.IntegerField(choices=DELETE_choice,default=LIVE)
    created_at=models.TimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

