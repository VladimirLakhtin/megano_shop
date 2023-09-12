from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from accounts.models import Avatar, Profile


class CreateUserSerializer(serializers.ModelSerializer):
    """
    Serializer for creating user and profile info.
    """

    class Meta:
        model = User
        fields = 'username', 'password', 'first_name',
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Profile.objects.create(
            user=user,
            fullName=validated_data.get('first_name'),
        )
        return user


class UpdatePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """

    model = User
    passwordCurrent = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    passwordReply = serializers.CharField(required=True)

    def validate(self, attrs):
        """Validate input passwords"""

        old_password = attrs.get('passwordCurrent')
        if not self.instance.check_password(old_password):
            msg = 'The current password is incorrect'
            raise ValidationError(msg)

        if attrs.get('password') != attrs.get('passwordReply'):
            msg = "Passwords don't match"
            raise ValidationError(msg)

        return attrs

    def update(self, instance, validate_data):
        instance.set_password(validate_data.get('password'))
        instance.save()
        return instance


class AvatarSerializer(serializers.ModelSerializer):
    """
    Serializer for user avatar reading and changing.
    """

    class Meta:
        model = Avatar
        fields = 'src', 'alt'
        read_only_fields = 'alt',

    def validate(self, attrs):
        """Validate file extension"""

        src = attrs.get('src')
        if not str(src).endswith(('.png', '.jpeg', '.jpg')):
            msg = "The file must have the following extensions: '.png', '.jpeg', '.jpg'"
            raise ValidationError(msg)
        return attrs

    def create(self, validated_data):
        avatar = Avatar.objects.create(src=validated_data.get('src'))
        profile = validated_data.get('profile')

        if profile.avatar.src != Avatar.default_path:
            profile.avatar.src.delete(save=False)
            profile.avatar.delete()

        profile.avatar = avatar
        profile.save()
        return avatar


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile info reading and changing.
    """
    avatar = AvatarSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = 'fullName', 'email', 'phone', 'avatar'
