from django.db import models
from datetime import datetime
from PIL import Image
from django.core.exceptions import ValidationError

from project.models import Project
# Create your models here.
def filepath_images(instance, filename):
    title = instance.product.name
    return 'products/%s-%s' % (title, filename)

def filepath_front_images(instance, filename):
    title = instance.name
    return 'products/%s-%s' % (title, filename)

def validate_image(value):
    if value.width != 1920 and value.height != 1080:
        raise ValidationError("The image should be in HD format (1920x1080)")
    else:
        return value

class Type(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=264)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=65)
    company = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    value = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    description = models.TextField(max_length=100000, default='')
    type = models.ForeignKey(Type, on_delete=models.SET(None))
    quantity = models.IntegerField(default=1)
    how_to_use = models.TextField(default='')
    front_images = models.ImageField(upload_to=filepath_front_images, default=None, validators=[validate_image])
    projects = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, default=None, null=True, related_name='city_product')

    def __str__(self):
        return self.name


    # def save(self):
    #     user = super(Product, self).save()
    #     try:
    #         image = Image.open(user.primaryphoto)
    #         resized_image = image.resize((1920, 1080), Image.ANTIALIAS)
    #         resized_image.save(user.primaryphoto.path)
    #     except:
    #         pass
    #     return user



class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images_product', validators=[validate_image])
    image = models.ImageField(upload_to=filepath_images)
    image_for = models.CharField(max_length=264, default=None)

    def __str__(self):
        return self.product.name

