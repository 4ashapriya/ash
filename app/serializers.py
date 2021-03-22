from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import User, BulkUser

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User  # model for serializer
        fields = ["username", "password", "email", "password2"]  # required fields

    def save(self):
        # user given email and username is vaildated and save it into the corresponding fields
        reg = User(

            email=self.validated_data['email'],
            username=self.validated_data['username'],
        )
        # manually check the password confirmation
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'password does not match'})
        reg.set_password(password)
        reg.save()
        return reg


class PermissionSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=300)

    class Meta:
        model = User
        fields = ["token"]


class UpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username'
        ]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class New(serializers.ModelSerializer):
    class Meta:
        model = User

        fields = '__all__'


class BulkSerializer(serializers.ModelSerializer):
    class Meta:
        model = BulkUser
        fields = '__all__'


class UserDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


User=get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):

    password2=serializers.CharField(style={'input_type':'password'},write_only=True)

    class Meta:
        model=User
        fields=["username","password","email","password2"]

    def save(self):
        reg=User(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
        )
        password=self.validated_data['password']
        password2=self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password':'password does not match'})
        reg.set_password(password)
        reg.save()
        return reg