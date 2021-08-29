from django.db import models
from store.models import Product,Variation
from accounts.models import Account
# Create your models here.

class Cart(models.Model): #class data model of the shopping cart
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):  # function to overrite the object name of this class
        return self.cart_id


class CartItem(models.Model):#class data model of the product in the cart
    user       = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    product    = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation, blank=True)
    cart       = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity   = models.IntegerField()
    is_active  = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price * self.quantity

    def __unicode__(self): # function to overrite the object name of this class
        return self.product
