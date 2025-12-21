
import os
import boto3
import mimetypes
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
MEDIA_ROOT = BASE_DIR / 'media'

def sync_media_to_r2():
    print("Starting upload of local media files to R2...")
    
    # R2 Configuration
    bucket_name = os.getenv('R2_BUCKET_NAME')
    endpoint_url = os.getenv('R2_ENDPOINT_URL')
    access_key = os.getenv('R2_ACCESS_KEY_ID')
    secret_key = os.getenv('R2_SECRET_ACCESS_KEY')
    
    if not all([bucket_name, endpoint_url, access_key, secret_key]):
        print("Error: Missing R2 environment variables.")
        return

    # Initialize S3 Client
    s3 = boto3.client(
        's3',
        endpoint_url=endpoint_url,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        config=boto3.session.Config(signature_version='s3v4'),
        region_name='auto'
    )

    # Walk through media directory
    count = 0
    for root, dirs, files in os.walk(MEDIA_ROOT):
        for file in files:
            local_path = os.path.join(root, file)
            relative_path = os.path.relpath(local_path, MEDIA_ROOT)
            s3_key = f"media/{relative_path}" # Prefix with media/ to match URL structure
            
            # Guess content type
            content_type, _ = mimetypes.guess_type(local_path)
            if content_type is None:
                content_type = 'application/octet-stream'
            
            print(f"Uploading: {s3_key}...")
            
            try:
                with open(local_path, 'rb') as f:
                    s3.upload_fileobj(
                        f, 
                        bucket_name, 
                        s3_key,
                        ExtraArgs={'ContentType': content_type, 'ACL': 'public-read'} # Assuming public read is desired or controlled by bucket policy
                    )
                count += 1
            except Exception as e:
                print(f"Failed to upload {s3_key}: {e}")

    print(f"\nSuccess! Uploaded {count} files to R2.")

if __name__ == "__main__":
    sync_media_to_r2()
