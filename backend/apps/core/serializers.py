from rest_framework import serializers

class URLSafeImageMixin:
    """
    A Mixin for DRF ModelSerializers that automatically strips out string URLs 
    passed to ImageFields or FileFields. 
    
    This is extremely useful when the frontend fetches data (receiving absolute URLs for images)
    and sends the entire object back via a PUT/PATCH request without uploading a new file.
    By dropping the string URL from the payload, DRF skips file validation on those fields
    and successfully performs a partial update on the text fields.
    """
    def to_internal_value(self, data):
        # Create a mutable copy if it's QueryDict/dict to avoid mutation errors
        if hasattr(data, 'copy'):
            data = data.copy()
            
        # Dynamically find all Image/File fields in this serializer
        for field_name, field in self.fields.items():
            if isinstance(field, (serializers.ImageField, serializers.FileField)):
                val = data.get(field_name)
                # If the field value is a string URL, pop it to ignore validation
                if isinstance(val, str) and val.startswith('http'):
                    data.pop(field_name)
                    
        return super().to_internal_value(data)
