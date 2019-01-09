from django.db import models
from product.models import Product
# Create your models here.
from django.core.validators import RegexValidator
from django.contrib.auth.models import User


class Status(models.Model):
    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=225, default='processing')
    def __str__(self):
        return self.status
#need to fix order serializer, need to add phone number to user, and add response in serializer
class OrderDetail(models.Model):
    id = models.AutoField(primary_key=True)
    address = models.TextField(default='', blank=True, null=False)
    city = models.CharField(max_length=255, default='', blank=True, null=False)
    postcode = models.IntegerField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    first_name = models.CharField(max_length=255, blank=False, null=False)
    last_name = models.CharField(max_length=255, blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=20, null=True, blank=True)
    status = models.ForeignKey(Status,default=1, related_name='order_status', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def orders(self):
        return self.order_set.all()

    def __str__(self):
        return self.email


class Order(models.Model):
    details = models.ForeignKey(OrderDetail,on_delete=models.CASCADE, related_name='orders')
    products = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=False, null=False)

    def __str__(self):
        return self.details.email

class Order_Product(models.Model):
    orders = models.ForeignKey(Order, on_delete=models.CASCADE)
    products = models.ForeignKey(Product, on_delete=models.CASCADE)

class Payment(models.Model):
    payment_ref = models.TextField()
    order = models.ForeignKey(OrderDetail, on_delete=models.CASCADE, default=None)
