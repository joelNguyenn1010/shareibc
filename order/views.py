from rest_framework.response import Response
from decimal import Decimal
from django.core.mail import send_mail
import sendgrid
from env.env import *
from sendgrid.helpers.mail import *
# Create your views here.
from rest_framework.generics import ListAPIView, CreateAPIView

from django.contrib.auth.models import User

import stripe

from shareibc.settings import STRIPE_SECRET_KEY

stripe.api_key = STRIPE_SECRET_KEY

from rest_framework import permissions, status
# Create your views here.
from product.models import Product
from .models import OrderDetail, Payment
from .serializers import OrderDetailsSerializer,DetailsSe


def countTotalPrice(orders):
    total_price = Decimal(0.0)
    for o in orders:
        k = Product.objects.filter(id=o.get('products')).values('price') #remember to change this back
        total_price+=(k.first().get('price')*o.get('quantity'))
    return int(total_price*100)

def changeQtyOrder(orders):
    for o in orders:
        try:
            product = Product.objects.get(pk=o.get('products'))
            product.quantity-=o.get('quantity')
            product.save()
        except:
            return Response(status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

def checkQtyOrder(orders):
    checking = True
    for o in orders:
        product = Product.objects.get(pk=o.get('products'))
        if product.quantity <= 0:
            checking = False
    return checking

def send_email(to, chargeid, id):
    print("SENDING EMAIL")
    # send_mail(
    #     'Order receipt',
    #     'Thanks for buying our product, your order id is %s-%s. This is automatic email, if there any issues, please contact our support' % (chargeid, id),
    #     'nguyenngocanh590@gmail.com',
    #     [to],
    #     fail_silently=False,
    # )
    sg = sendgrid.SendGridAPIClient(apikey=SENDGRID)
    from_email = Email("contact@shareibc.com")
    to_email = Email(to)
    subject = "Order receipt"
    content = Content("text/plain", 'Thanks for buying our product, your order id is %s-%s. This is automatic email, if there any issues, please contact our support' % (chargeid, id))
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)

class OrderCreateAPI(CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = OrderDetailsSerializer

    def post(self, request,*args, **kwargs):
        orders = request.data['orders']
        try:
            total_price = countTotalPrice(orders)
        except:
            return Response({"Error":"Your order is no longer exist"}, status=status.HTTP_410_GONE)
        token = request.data.pop('token')
        details = OrderDetailsSerializer(data=request.data)
        if details.is_valid():
            if len(orders) > 0 and checkQtyOrder(orders):
                try:
                    email = request.data['email']
                    charge = stripe.Charge.create(
                           amount=total_price,
                           currency="usd",
                           source= token,
                           description="The product charged to the user",
                           receipt_email=details.data.get('email')
                      )
                    # print(charge)
                    orderDetail = self.create(request, *args, **kwargs)
                    new_order = OrderDetail.objects.get(id=orderDetail.data.get('id'))
                    Payment.objects.create(payment_ref=charge.get("id"), order=new_order)
                    changeQtyOrder(orders)
                    user = request.user
                    print(user)
                    if request.user.is_authenticated:
                            new_order.user = user
                            new_order.save()
                    orderDetail.data.pop('orders')
                    try:
                        send_email(email,charge.get("id"), orderDetail.data.get('id'))
                    except:
                        pass
                    return orderDetail
                except Exception as e:
                    content = {'Error': 'Your card has been declined, please try again'}
                    return Response(content)
            else:
                content = {'Error': 'The order is no longer available'}
                return Response(content, status=status.HTTP_424_FAILED_DEPENDENCY)
        else:
            content = {'Error' : 'The shipping is required'}
            return Response(content,status=status.HTTP_406_NOT_ACCEPTABLE)



class OrderAPI(ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = DetailsSe
    queryset = OrderDetail.objects.all()

    def get_queryset(self):
        print(self.request.user)
        #will return the user
        # print(unicode(request.auth))
        user = User.objects.get(username=self.request.user)
        order = OrderDetail.objects.filter(user=user)
        # print(order.order_set.all())
        return order


