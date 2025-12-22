"""
Views for Admin Authentication.
"""

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from django.conf import settings

from .serializers import (
    AdminLoginSerializer,
    AdminUserSerializer,
    LogoutSerializer,
)
from .permissions import IsAdminUser
from .utils import (
    set_refresh_token_cookie,
    delete_refresh_token_cookie,
    get_refresh_token_from_cookie,
)


from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

@method_decorator(csrf_exempt, name='dispatch')
class AdminLoginView(APIView):
    """
    Admin Login Endpoint.
    
    POST /api/admin/auth/login/
    
    Authenticates admin user and returns:
    - Access token in response body
    - Refresh token in HTTP-only cookie
    """
    permission_classes = [AllowAny]
    serializer_class = AdminLoginSerializer
    
    def post(self, request):
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )
        
        if not serializer.is_valid():
            return Response(
                {
                    'success': False,
                    'message': serializer.errors.get('detail', ['Invalid credentials'])[0] 
                               if isinstance(serializer.errors.get('detail'), list)
                               else serializer.errors.get('detail', 'Invalid credentials'),
                    'errors': serializer.errors,
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        user = serializer.validated_data['user']
        
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        
        # Prepare response
        user_serializer = AdminUserSerializer(user)
        response_data = {
            'success': True,
            'message': 'Login successful',
            'user': user_serializer.data,
            'access': access_token,
        }
        
        response = Response(response_data, status=status.HTTP_200_OK)
        
        # Set refresh token in HTTP-only cookie
        set_refresh_token_cookie(response, refresh)
        
        return response


class AdminLogoutView(APIView):
    """
    Admin Logout Endpoint.
    
    POST /api/admin/auth/logout/
    
    Blacklists the refresh token and clears the cookie.
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def post(self, request):
        try:
            # Get refresh token from cookie
            refresh_token = get_refresh_token_from_cookie(request)
            
            if refresh_token:
                # Blacklist the refresh token
                token = RefreshToken(refresh_token)
                token.blacklist()
            
            response = Response(
                {
                    'success': True,
                    'message': 'Logged out successfully',
                },
                status=status.HTTP_200_OK
            )
            
            # Delete the refresh token cookie
            delete_refresh_token_cookie(response)
            
            return response
            
        except TokenError:
            # Token already blacklisted or invalid
            response = Response(
                {
                    'success': True,
                    'message': 'Logged out successfully',
                },
                status=status.HTTP_200_OK
            )
            delete_refresh_token_cookie(response)
            return response


class TokenRefreshView(APIView):
    """
    Token Refresh Endpoint.
    
    POST /api/admin/auth/refresh/
    
    Uses refresh token from HTTP-only cookie to issue new access token.
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        # Get refresh token from cookie
        refresh_token = get_refresh_token_from_cookie(request)
        
        if not refresh_token:
            return Response(
                {
                    'success': False,
                    'message': 'Refresh token not found',
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        try:
            # Validate the refresh token
            refresh = RefreshToken(refresh_token)
            
            # If ROTATE_REFRESH_TOKENS is True, create new refresh token BEFORE blacklisting old one
            if settings.SIMPLE_JWT.get('ROTATE_REFRESH_TOKENS', False):
                from django.contrib.auth import get_user_model
                User = get_user_model()
                user_id = refresh.payload.get('user_id')
                
                try:
                    user = User.objects.get(id=user_id)
                    # Create new refresh token FIRST
                    new_refresh = RefreshToken.for_user(user)
                    # Get access token from the NEW refresh token
                    access_token = str(new_refresh.access_token)
                    
                    response_data = {
                        'success': True,
                        'access': access_token,
                    }
                    
                    response = Response(response_data, status=status.HTTP_200_OK)
                    
                    # Set new refresh token cookie
                    set_refresh_token_cookie(response, new_refresh)
                    
                    # NOW blacklist the old token (after new one is ready)
                    if settings.SIMPLE_JWT.get('BLACKLIST_AFTER_ROTATION', True):
                        try:
                            refresh.blacklist()
                        except AttributeError:
                            pass
                    
                    return response
                    
                except User.DoesNotExist:
                    return Response(
                        {
                            'success': False,
                            'message': 'User not found',
                        },
                        status=status.HTTP_401_UNAUTHORIZED
                    )
            else:
                # No rotation - just get access token from existing refresh token
                access_token = str(refresh.access_token)
                
                response_data = {
                    'success': True,
                    'access': access_token,
                }
                
                return Response(response_data, status=status.HTTP_200_OK)
            
        except TokenError as e:
            # Clear the invalid/expired cookie so the browser stops sending it
            response = Response(
                {
                    'success': False,
                    'message': 'Invalid or expired refresh token',
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
            delete_refresh_token_cookie(response)
            return response



class AdminMeView(APIView):
    """
    Get Current Admin User Endpoint.
    
    GET /api/admin/auth/me/
    
    Returns the currently authenticated admin user's details.
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get(self, request):
        serializer = AdminUserSerializer(request.user)
        return Response(
            {
                'success': True,
                'user': serializer.data,
            },
            status=status.HTTP_200_OK
        )


class AdminVerifyTokenView(APIView):
    """
    Verify Token Endpoint.
    
    POST /api/admin/auth/verify/
    
    Verifies if the access token is valid.
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def post(self, request):
        return Response(
            {
                'success': True,
                'message': 'Token is valid',
                'user': AdminUserSerializer(request.user).data,
            },
            status=status.HTTP_200_OK
        )
