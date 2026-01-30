"""
Serializers for Admin Authentication.
"""

from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import AdminUser


class AdminLoginSerializer(serializers.Serializer):
    """
    Serializer for admin login.
    Validates email and password and returns the authenticated user.
    """
    email = serializers.EmailField(
        required=True,
        error_messages={
            'required': 'Email is required.',
            'invalid': 'Enter a valid email address.',
        }
    )
    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'},
        error_messages={
            'required': 'Password is required.',
        }
    )
    
    def validate(self, attrs):
        email = attrs.get('email', '').lower().strip()
        password = attrs.get('password', '')
        
        if not email or not password:
            raise serializers.ValidationError(
                {'detail': 'Email and password are required.'},
                code='authorization'
            )
        
        # Authenticate user
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        
        if not user:
            raise serializers.ValidationError(
                {'detail': 'Invalid email or password.'},
                code='authorization'
            )
        
        if not user.is_active:
            raise serializers.ValidationError(
                {'detail': 'This account has been deactivated.'},
                code='authorization'
            )
        
        if not user.is_staff:
            raise serializers.ValidationError(
                {'detail': 'You do not have admin access.'},
                code='authorization'
            )
        
        attrs['user'] = user
        return attrs


class AdminUserSerializer(serializers.ModelSerializer):
    """
    Serializer for AdminUser model.
    Used for returning user data in responses.
    """
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = AdminUser
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'full_name',
            'role',
            'is_active',
            'date_joined',
            'last_login',
        ]
        read_only_fields = ['id', 'date_joined', 'last_login']
    
    def get_full_name(self, obj):
        return obj.get_full_name()


class AdminUserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating new admin users.
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'},
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
    )
    
    class Meta:
        model = AdminUser
        fields = [
            'email',
            'first_name',
            'last_name',
            'password',
            'password_confirm',
            'role',
        ]
    
    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password_confirm'):
            raise serializers.ValidationError(
                {'password_confirm': 'Passwords do not match.'}
            )
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        
        user = AdminUser.objects.create_user(
            password=password,
            **validated_data
        )
        return user


class TokenRefreshResponseSerializer(serializers.Serializer):
    """
    Serializer for token refresh response.
    """
    access = serializers.CharField()


class LogoutSerializer(serializers.Serializer):
    """
    Serializer for logout - expects refresh token.
    """
    refresh = serializers.CharField(required=False)
