"""
Utility functions for authentication.
"""

from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings


def custom_exception_handler(exc, context):
    """
    Custom exception handler that returns consistent error responses.
    """
    response = exception_handler(exc, context)
    
    if response is not None:
        custom_response_data = {
            'success': False,
            'message': 'An error occurred.',
            'errors': {},
        }
        
        if isinstance(response.data, dict):
            # Handle 'detail' key (common in DRF)
            if 'detail' in response.data:
                custom_response_data['message'] = str(response.data['detail'])
            else:
                custom_response_data['errors'] = response.data
                # Try to get a meaningful message
                for key, value in response.data.items():
                    if isinstance(value, list) and len(value) > 0:
                        custom_response_data['message'] = str(value[0])
                        break
                    elif isinstance(value, str):
                        custom_response_data['message'] = value
                        break
        elif isinstance(response.data, list):
            custom_response_data['message'] = str(response.data[0]) if response.data else 'An error occurred.'
        
        response.data = custom_response_data
    
    return response


def set_refresh_token_cookie(response, refresh_token):
    """
    Set the refresh token as an HTTP-only cookie.
    """
    response.set_cookie(
        key=settings.REFRESH_TOKEN_COOKIE_NAME,
        value=str(refresh_token),
        httponly=settings.REFRESH_TOKEN_COOKIE_HTTPONLY,
        secure=settings.REFRESH_TOKEN_COOKIE_SECURE,
        samesite=settings.REFRESH_TOKEN_COOKIE_SAMESITE,
        path=settings.REFRESH_TOKEN_COOKIE_PATH,
        max_age=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds(),
    )
    return response


def delete_refresh_token_cookie(response):
    """
    Delete the refresh token cookie (for logout).
    """
    response.delete_cookie(
        key=settings.REFRESH_TOKEN_COOKIE_NAME,
        path=settings.REFRESH_TOKEN_COOKIE_PATH,
    )
    return response


def get_refresh_token_from_cookie(request):
    """
    Get the refresh token from the HTTP-only cookie.
    """
    return request.COOKIES.get(settings.REFRESH_TOKEN_COOKIE_NAME)
