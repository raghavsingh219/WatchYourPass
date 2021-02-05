from rest_framework import serializers
from rest_framework.serializers import Serializer, FileField
from .models import Domain, BreachedSite, Password, Account
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user


class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = ('domain', 'count',)


class Breached_SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = BreachedSite
        fields = ('domain', 'breach_type', 'account_breach_count',)


class PasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Password
        fields = ('hash', 'count',)


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('email', 'domain', 'breached_site', 'passwords', 'count',)


class UploadSerializer(Serializer):
    file_uploaded = FileField()
    class Meta:
        fields = ['file_uploaded']