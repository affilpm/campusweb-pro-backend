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
        
        # Prepare response - include refresh token in body for cross-origin compatibility
        user_serializer = AdminUserSerializer(user)
        response_data = {
            'success': True,
            'message': 'Login successful',
            'user': user_serializer.data,
            'access': access_token,
            'refresh': str(refresh),  # Include refresh token in body for localStorage storage
        }
        
        response = Response(response_data, status=status.HTTP_200_OK)
        
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
            # Get refresh token from request body
            refresh_token = request.data.get('refresh')
            
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
            return response


from rest_framework_simplejwt.views import TokenRefreshView as SimpleTokenRefreshView

@method_decorator(csrf_exempt, name='dispatch')
class TokenRefreshView(SimpleTokenRefreshView):
    """
    Token Refresh Endpoint.
    
    POST /api/admin/auth/refresh/
    
    Uses refresh token from body to issue new access token.
    Inherits from SimpleJWT's TokenRefreshView for robust handling of rotation and blacklisting.
    """
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            if response.status_code == 200:
                response.data['success'] = True
            return response
        except (TokenError, InvalidToken):
            return Response(
                {
                    'success': False,
                    'message': 'Invalid or expired refresh token',
                },
                status=status.HTTP_401_UNAUTHORIZED
            )



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
