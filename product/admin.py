from django.contrib import admin
from .models import Product, Type, ProductImage, City
# Register your models here.

class ImageInLine(admin.TabularInline):
    model = ProductImage

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'price', 'value', 'type', 'city')
    list_filter = ('company', 'type__name', 'city')
    inlines = [ImageInLine,]


admin.site.register(Product, ProductAdmin)
admin.site.register(Type)
admin.site.register(ProductImage)
admin.site.register(City)

