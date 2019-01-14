from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework import permissions, status
from django.core.mail import send_mail,mail_admins
import sendgrid
from env.env import *
from sendgrid.helpers.mail import *

# Create your views here.
from .serializers import RegisterSerializer, UserSupportSerializer, UpdateSerializer,RetrieveUserSerializer
from django.contrib.auth import authenticate, get_user_model
from .models import UserProfile
User = get_user_model()

class AuthView(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request, *args, **kwargs):
        return Response({'token' 'abx'})

class RegisterAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

def send_email(message, inquiry, email, name):
    print("SENDING EMAIL")
    # sg = sendgrid.SendGridAPIClient(apikey=SENDGRID)
    # from_email = Email("contact@shareibc.com")
    # to_email = Email("contact@shareibc.com")
    # subject = "%s - %s - %s" % (inquiry, name, email)
    # print(message)
    # content = Content("text/plain", message)
    # mail = Mail(from_email, subject, to_email, content)
    # response = sg.client.mail.send.post(request_body=mail.get())
    # print(response.status_code)
    # print(response.body)
    send_mail(
        '%s - %s - %s' % (inquiry, name, email),
        '%s' % (message),
        '%s' % (email),
        ['nguyenngocanh590@gmail.com'],
        # fail_silently=False,
    )

class AuthVerify(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        if request.user.is_authenticated:
            return Response({"success:success"}, status=status.HTTP_200_OK)
        else:
            return Response({"Error: Not auth"}, status=status.HTTP_401_UNAUTHORIZED)

class UserSupport(CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSupportSerializer

    def post(self, request, *args, **kwargs):
        se = UserSupportSerializer(data=request.data)
        if se.is_valid():
            support_created = self.create(request, *args, **kwargs)
            send_email(request.data['message'], request.data['inquiry'], request.data['email'], request.data['first_name'] + request.data['last_name'])
            return support_created
        else:
            return Response(se.errors)

class UpdateUser(APIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UpdateSerializer

    def put(self, request, *args, **kwargs):
        user = User.objects.get(username=request.user)
        se = UpdateSerializer(data=request.data)
        if se.is_valid():
            user.first_name = request.data["first_name"]
            user.last_name = request.data["last_name"]
            phone = request.data['userprofile'].get('phone_number')
            try:
                profile = UserProfile.objects.get(user=user)
                profile.phone_number = phone
                profile.save()
            except:
                UserProfile.objects.create(
                    phone_number=phone,
                    user=user
                )
            # if not profile:
            #     UserProfile.objects.create(
            #         phone_number=phone,
            #         user=user
            #     )
            #     print('True')
            # else:
            #     profile.phone_number = phone
            #     profile.save()
            user.save()
            return Response(se.data, status=status.HTTP_200_OK)
        else:
            return Response(se.errors, status=status.HTTP_400_BAD_REQUEST)

class UserAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = RetrieveUserSerializer

    def get(self, request):
        user = request.user
        se = RetrieveUserSerializer(user)
        return Response(se.data)
