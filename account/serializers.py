from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.core.exceptions import ValidationError

from account.models import User


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'phone',
            'first_name',
            'last_name',
            'avatar',
            'last_login',
        )


class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(validators=[validate_password])

    class Meta:
        model = User
        fields = (
            'email',
            'phone',
            'first_name',
            'last_name',
            'avatar',
            'password'
        )
        extra_kwargs = {
            'last_name': {'required': True},
            'first_name': {'required': True},
            'phone': {'required': True},
        }

    def validate(self, attrs):
        cop = attrs.copy()
        cop.pop('avatar')
        for item in cop.items():
            if not item[1]:
                raise ValidationError({
                    item[0]: [
                        f'{item[0]} could not be empty'
                    ]
                })
        return attrs

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    old_password = serializers.CharField(required=True,)
    new_password = serializers.CharField(required=True, validators=[validate_password])


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'password', 'phone', 'avatar',)

    def validate(self, attrs):
        cop = attrs.copy()
        cop.pop('avatar')
        for item in cop.items():
            if not item[1]:
                raise ValidationError({
                    item[0]: [
                        f'{item[0]} could not be empty'
                    ]
                })
        return attrs


class SendResetPasswordKeySerializer(serializers.Serializer):

    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):

    key = serializers.UUIDField()
    new_password = serializers.CharField(validators=[validate_password])