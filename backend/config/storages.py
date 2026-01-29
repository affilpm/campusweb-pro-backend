from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings


class R2MediaStorage(S3Boto3Storage):
    """
    Dedicated Cloudflare R2 storage backend for Media.
    """
    location = 'media'
    default_acl = None
    file_overwrite = False
    querystring_auth = False
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Optimize R2 connection settings
        from botocore.config import Config
        self.config = Config(
            signature_version='s3v4',
            connect_timeout=15,
            read_timeout=30,
            retries={'max_attempts': 3}
        )


class R2StaticStorage(S3Boto3Storage):
    """
    Dedicated Cloudflare R2 storage backend for Static files.
    """
    location = 'static'
    default_acl = None
    file_overwrite = True
    querystring_auth = False
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Optimize R2 connection settings
        from botocore.config import Config
        self.config = Config(
            signature_version='s3v4',
            connect_timeout=15,
            read_timeout=30,
            retries={'max_attempts': 3}
        )
