from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from .models import UserProfile, UserSupport
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER
User = get_user_model()

class UserSupportSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSupport
        fields = '__all__'

    def create(self, valid, *args, **kwargs):
        request = self._context.get("request")
        if request.user.is_authenticated:
            valid.pop('user')
            user = UserSupport.objects.create(
                **valid,
                user=request.user
            )
            return user
        else:
            user = UserSupport.objects.create(
                **valid
            )
            return user



class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('phone_number',)
        # read_only_fields = ('user',)

class RetrieveUserSerializer(serializers.ModelSerializer):
    userprofile = ProfileSerializer()
    class Meta:
        model = User
        fields = ('email','first_name','last_name','userprofile')


class RegisterSerializer(serializers.ModelSerializer):
    userprofile = ProfileSerializer()
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('username','first_name','last_name','email', 'password', 'password2', 'token','userprofile')
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        qs = User.objects.filter(email__iexact = value)
        if qs.exists():
            raise serializers.ValidationError('User with this email already exists')
        return value

    def validate_username(self, value):
        qs = User.objects.filter(username__iexact=value)
        if qs.exists():
            raise serializers.ValidationError('User with this username already exists')
        return value
    def get_token(self, obj):
        user = obj
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return token

    def validate(self, data):
        pw = data.get('password')
        pw2 = data.get('password2')
        if pw != pw2:
            raise serializers.ValidationError("Password must match")
        return data

    def create(self, vali_data):
        profiles = vali_data.pop('userprofile')
        user = User(
            username=vali_data.get('username'),
            email=vali_data.get('email'),
            first_name=vali_data.get('first_name'),
            last_name=vali_data.get('last_name'),
        )
        user.set_password(vali_data.get('password'))
        user.save()
        try:
            UserProfile.objects.create(
                **profiles,
                user=user
            )
        except Exception as e:
            raise serializers.ValidationError("Fail to create profile")
        return user

class UpdateSerializer(serializers.ModelSerializer):
    userprofile = ProfileSerializer()
    class Meta:
        model = User
        fields = ('first_name','last_name','userprofile')

