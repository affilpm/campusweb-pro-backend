from rest_framework import serializers
from apps.core.serializers import URLSafeImageMixin

from .models import GalleryCategory, GalleryImage

class GalleryCategoryPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryCategory
        fields = ['id', 'name', 'slug']

class GalleryImagePublicSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_slug = serializers.CharField(source='category.slug', read_only=True)
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = GalleryImage
        fields = ['id', 'title', 'image', 'caption', 'category', 'category_name', 'category_slug', 'created_at']
        
    def get_image(self, obj):
        if obj.image:
            return obj.image.url
        return None

class GalleryCategoryAdminSerializer(URLSafeImageMixin, serializers.ModelSerializer):
    class Meta:
        model = GalleryCategory
        fields = '__all__'

class GalleryImageAdminSerializer(URLSafeImageMixin, serializers.ModelSerializer):
    class Meta:
        model = GalleryImage
        fields = '__all__'
