from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import User


class ObtainTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.CharField()
    password = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username", "password"]

    def create(self, validated_data):
        user = User.objects.create(email=validated_data['email'],
                                   username=validated_data['username']
                                   )
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    # token = serializers.CharField(max_length=255, read_only=True)
    #
    # def validate(self, data):
    #     email = data.get('email', None)
    #     username = data.get('username', None)
    #     password = data.get('password', None)
    #     if email is None:
    #         raise serializers.ValidationError(
    #             'An email address is required to log in.'
    #         )
    #     if password is None:
    #         raise serializers.ValidationError(
    #             'A password is required to log in.'
    #         )
    #     user = authenticate(username=username, email=email, password=password)
    #     if user is None:
    #         raise serializers.ValidationError(
    #             'A user with this email and password was not found.'
    #         )
    #     if not user.is_active:
    #         raise serializers.ValidationError(
    #             'This user has been deactivated.'
    #         )
    #     return {
    #         'email': user.email,
    #         'username': user.username,
    #         'token': user.token
    #     }
