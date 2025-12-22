from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings


class CloudFrontMediaStorage(S3Boto3Storage):
    """
    Media storage backend that uploads to S3 and serves via CloudFront.
    """
    location = 'media'
    default_acl = None
    file_overwrite = False
    custom_domain = getattr(settings, 'CLOUDFRONT_DOMAIN', None)
    
    def __init__(self, *args, **kwargs):
        # Allow bucket_name to be passed from STORAGES config
        if 'bucket_name' in kwargs:
            self.bucket_name = kwargs.pop('bucket_name')
        if 'location' in kwargs:
            self.location = kwargs.pop('location')
        if 'file_overwrite' in kwargs:
            self.file_overwrite = kwargs.pop('file_overwrite')
        super().__init__(*args, **kwargs)


class StaticStorage(S3Boto3Storage):
    """
    Static files storage backend (optional, for production).
    """
    location = 'static'
    default_acl = None
