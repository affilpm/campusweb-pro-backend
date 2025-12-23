import os
import django
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

print("--- DEBUGGING S3 CONFIGURATION ---")
print(f"AWS_ACCESS_KEY_ID: {settings.AWS_ACCESS_KEY_ID[:4]}****")
print(f"AWS_STORAGE_BUCKET_NAME: {settings.AWS_STORAGE_BUCKET_NAME}")
print(f"AWS_S3_REGION_NAME: {settings.AWS_S3_REGION_NAME}")
print(f"DEFAULT_FILE_STORAGE: {settings.DEFAULT_FILE_STORAGE}")
print(f"CLOUDFRONT_DOMAIN: {getattr(settings, 'CLOUDFRONT_DOMAIN', 'Not Set')}")

print("\n--- ATTEMPTING UPLOAD ---")
try:
    file_name = 'debug_test_file.txt'
    content = b'This is a test upload from the debug script.'
    path = default_storage.save(file_name, ContentFile(content))
    
    print(f"✅ SUCCESS! File saved to: {path}")
    print(f"URL: {default_storage.url(path)}")
except Exception as e:
    print(f"❌ FAILED! Error type: {type(e).__name__}")
    print(f"Error message: {str(e)}")
