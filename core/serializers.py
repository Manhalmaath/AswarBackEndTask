import base64
import re
from hashlib import sha256

from cryptography.fernet import Fernet
from django.conf import settings
from rest_framework import serializers

from core.models import Credential, Service, Tag


def validate_password(value):
    if len(value) < 8:
        raise serializers.ValidationError("Password must be at least 8 characters long.")
    if not re.search(r'[A-Z]', value):
        raise serializers.ValidationError("Password must contain at least one uppercase letter.")
    if not re.search(r'[a-z]', value):
        raise serializers.ValidationError("Password must contain at least one lowercase letter.")
    if not re.search(r'[0-9]', value):
        raise serializers.ValidationError("Password must contain at least one digit.")
    if not re.search(r'[\W_]', value):
        raise serializers.ValidationError("Password must contain at least one special character.")
    return value


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    password1 = serializers.CharField(validators=[validate_password])
    password2 = serializers.CharField(validators=[validate_password])
    first_name = serializers.CharField()
    last_name = serializers.CharField()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        exclude = ['created_by']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        exclude = ['created_by']


class CredentialSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Credential
        exclude = ['created_by']

    def create(self, validated_data):
        password = validated_data.pop('password')
        key = base64.urlsafe_b64encode(sha256(settings.SECRET_KEY.encode()).digest())
        cipher_suite = Fernet(key)
        encrypted_password = cipher_suite.encrypt(password.encode())
        validated_data['password'] = encrypted_password.decode()
        return super().create(validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            key = base64.urlsafe_b64encode(sha256(settings.SECRET_KEY.encode()).digest())
            cipher_suite = Fernet(key)
            encrypted_password = cipher_suite.encrypt(password.encode())
            validated_data['password'] = encrypted_password.decode()
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        key = base64.urlsafe_b64encode(sha256(settings.SECRET_KEY.encode()).digest())
        cipher_suite = Fernet(key)
        decrypted_password = cipher_suite.decrypt(instance.password.encode()).decode()
        representation['password'] = decrypted_password
        return representation
