from rest_framework import serializers
from .models import Product, ProductImage, City

class ImageSeriallizer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('image', 'image_for')

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    images_product = ImageSeriallizer(many=True)
    # city_product = CitySerializer(many=True)
    class Meta:
        model = Product
        fields = ('id','name','how_to_use', 'company', 'price', 'value', 'description','date', 'type', 'quantity', 'front_images','images_product','city')
        depth = 1


class ProductIndexSerializer(serializers.ModelSerializer):
    images_product = ImageSeriallizer(many=True)
    # city_product = CitySerializer(many=True)
    class Meta:
        model = Product
        fields = ('id','name', 'company', 'price', 'value','date', 'type', 'quantity', 'front_images','city')
        depth = 1