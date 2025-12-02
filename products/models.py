from django.db import models

# Create your models here.
CATEGORY_CHOICES = (
    ('fruit', 'Fruit'),
    ('vegetable', 'Vegetable'),
    ('other', 'Other'),
)

class Product(models.Model):
    LIVE=1
    DELETE=0
    DELETE_choice=((LIVE,'live'),(DELETE,'delete'))
    name=models.CharField(max_length=20)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    description=models.TextField()
    image=models.ImageField(upload_to='products/')
    priority=models.IntegerField(default=0)
    delete_status=models.IntegerField(choices=DELETE_choice,default=LIVE)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    created_at=models.TimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)



    def __str__(self):
        return self.name


