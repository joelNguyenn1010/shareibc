from django.contrib import admin, messages

# Register your models here.
from .models import Order, OrderDetail, Status, Payment
from product.models import Product


# def changeQtyOrder(orders):
#     for o in orders:
#         try:
#             product = Product.objects.get(pk=o.get('products'))
#             product.quantity-=o.get('quantity')
#             product.save()
#         except:
#             return Response(status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
#



admin.site.disable_action('delete_selected')

class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name', 'email','phone_number','status','user']
    actions = ['make_delivery', 'make_refund']

    def make_delivery(self, request, queryset):
        # print(queryset.values('id'))
        queryset.update(status='2')
        self.message_user(request, "Success")
    make_delivery.short_description = "Mark order status delivery"

    def make_refund(self, request, queryset):
        for o in queryset.values('id','status'):
            if o.get('status') != 4:
                order = Order.objects.get(details__id=o.get('id'))
                product = Product.objects.get(id=order.products.id)
                order.products.quantity += order.quantity
                order.products.save()
                queryset.update(status='4')
            else:
                messages.error(request, "The order %s is already refunded" % o.get('id'))
    make_refund.short_description = "Mark order status refund"

class StatusAdmin(admin.ModelAdmin):
    list_display = ['id','status']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['details','products','quantity']

admin.site.register(Order,OrderAdmin)
admin.site.register(OrderDetail, OrderDetailAdmin)
admin.site.register(Payment)
admin.site.register(Status,StatusAdmin)
