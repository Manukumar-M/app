from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
from .models import CustomUser

# serializers.py
class UserSignupSerializer(serializers.ModelSerializer):
 
 from django.contrib.auth import get_user_model
User = get_user_model()

class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'phone_number', 'password', 'web_terms', 'dataprocessing', 'subscription']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        user = CustomUser.objects.create(**validated_data)
        return user


from rest_framework import serializers
class UserSignInSerializer(serializers.Serializer):
    identifier = serializers.CharField()
    password = serializers.CharField()
    print("Identifier:", identifier)
    print("Password:", password)
    print("User:", User)

    def validate(self, data):
        identifier = data.get('identifier')
        password = data.get('password')

        try:
            user = CustomUser.objects.filter(
                Q(username__iexact=identifier) |
                Q(email__iexact=identifier) |
                Q(phone_number__iexact=identifier)
            ).first()

            print("User:", user)  # Add this print statement
            if user and user.is_active and user.check_password(password):
                return user
            else:
                raise serializers.ValidationError("Invalid credentials")
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Invalid credentials")