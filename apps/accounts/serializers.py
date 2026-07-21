from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone_number', 'role']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    email = serializers.EmailField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message='Email already registered.'
            )
        ]
    )
    role = serializers.ChoiceField(
        choices=User.ROLE_CHOICES,
        required=False,
        default=User.BUYER
    )
    phone_number = serializers.CharField(required=False, allow_blank=True, max_length=15)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role', 'phone_number']

    def validate_phone_number(self, value):
        if not value:
            return value
        normalized = value.strip()
        return normalized

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
