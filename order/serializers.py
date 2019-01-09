from rest_framework import serializers
from .models import Order, OrderDetail
from rest_framework.response import Response

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['details','products', 'quantity']
        read_only_fields = ('details',)

#this class is for checking the orders array on the client side
class OrdersProductSerialer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['products', 'quantity']
        # read_only_fields = ('details',)
        depth = 1
#this class is for order of the user
class DetailsSe(serializers.ModelSerializer):
    orders = OrdersProductSerialer(many=True)
    class Meta:
        model = OrderDetail
        fields = ['id','phone_number','address','city','postcode','first_name','last_name','email','total_price','status', 'orders']
        depth = 1
#this class is for create order
class OrderDetailsSerializer(serializers.ModelSerializer):
    orders = OrderSerializer(many=True)
    class Meta:
        model = OrderDetail
        fields = ['id','phone_number','address','city','postcode','first_name','last_name','email','total_price', 'orders','status']

    def create(self, validated_data):
        orders = validated_data.pop('orders')
        if len(orders) == 0:
            raise serializers.ValidationError("Error occur")
        else:
            try:
                orderDetails = OrderDetail(**validated_data)
                orderDetails.save()
            except:
                raise serializers.ValidationError("Error occur")
            for order in orders:
                Order.objects.create(**order, details=orderDetails)
            return orderDetails


