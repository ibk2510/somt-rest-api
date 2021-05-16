from .models import Consumer, Address, Subscription
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password', 'email', 'first_name', 'last_name']


class ConsumerSerializer(serializers.ModelSerializer):
    user_address = AddressSerializer()
    user = UserSerializer()

    class Meta:
        model = Consumer
        fields = ['phone', 'user', 'user_address']

    def create(self, validated_data):

        # print(validated_data)
        pwd = validated_data.get('user').get('password')
        related_user = UserSerializer(data=dict(validated_data.pop('user')))
        if related_user.is_valid():
            related_user = related_user.save()
            related_user.username = related_user.email
            related_user.set_password(pwd)
            related_user.save()


        else:
            print(related_user.errors)
        related_address = AddressSerializer(data=dict(validated_data.pop('user_address')))
        if related_address.is_valid():
            related_address = related_address.save()
        else:
            print(related_address.errors)

        instance = Consumer.objects.create(
            user=related_user,
            user_address=related_address,
            phone=validated_data['phone']
        )

        return instance


class SubscriptionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'





class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        user = authenticate(username=email, password=password)
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password is not found.'
            )
        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'User with given email and password does not exists'
            )
        return {
            'email': user.email,
            'token': jwt_token
        }
