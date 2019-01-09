from django.contrib import admin
from .models import UserProfile, UserSupport
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(UserSupport)