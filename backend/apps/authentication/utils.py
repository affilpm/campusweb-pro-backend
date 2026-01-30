"""
Utility functions for authentication.
"""

from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings


def custom_exception_handler(exc, context):
    """
    Custom exception handler that returns consistent error responses and logs 500s.
    """
    import logging
    logger = logging.getLogger('django')
    
    response = exception_handler(exc, context)
    
    if response is None:
        # This is a 500 internal server error
        logger.error(f"Internal Server Error: {str(exc)}", exc_info=True)
        return Response(
            {
                'success': False,
                'message': 'An internal server error occurred. Our team has been notified.',
                'errors': {'detail': str(exc) if settings.DEBUG else 'Internal server error'},
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    if response is not None:
        custom_response_data = {
            'success': False,
            'message': 'An error occurred.',
            'errors': {},
        }
        if isinstance(response.data, dict):
            if 'detail' in response.data:
                custom_response_data['message'] = str(response.data['detail'])
            else:
                custom_response_data['errors'] = response.data
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


