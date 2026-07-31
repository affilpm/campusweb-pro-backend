import os
import django
import re
from io import BytesIO
from PIL import Image

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from apps.core.management.commands.seed_data import Command

# Find all placeholder strings in seed_data.py
with open("apps/core/management/commands/seed_data.py", "r") as f:
    content = f.read()

placeholders = re.findall(r'"(placeholder/[^"]+)"', content)
placeholders = list(set(placeholders))

print(f"Found {len(placeholders)} unique placeholders.")

for p in placeholders:
    if not default_storage.exists(p):
        print(f"Creating dummy for {p}...")
        img_format = 'PNG' if p.endswith('.png') else 'JPEG'
        mode = 'RGBA' if img_format == 'PNG' else 'RGB'
        img = Image.new(mode, (800, 600), color=(200, 200, 200))
        
        img_io = BytesIO()
        img.save(img_io, format=img_format)
        
        default_storage.save(p, ContentFile(img_io.getvalue()))
    else:
        print(f"{p} already exists.")

print("Done creating dummy images.")
