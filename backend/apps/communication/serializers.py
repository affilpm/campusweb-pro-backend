from rest_framework import serializers
from apps.core.serializers import URLSafeImageMixin

from .models import Notice, Event

class NoticePublicSerializer(serializers.ModelSerializer):
    attachment = serializers.SerializerMethodField()
    
    class Meta:
        model = Notice
        fields = ['id', 'title', 'slug', 'content', 'attachment', 'is_important', 'publish_date', 'status']
        
    def get_attachment(self, obj):
        if obj.attachment:
            return obj.attachment.url
        return None

class EventPublicSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = Event
        fields = ['id', 'title', 'slug', 'excerpt', 'content', 'image', 'event_date', 'is_featured']
        
    def get_image(self, obj):
        if obj.image:
            return obj.image.url
        return None

# Admin Serializers
class NoticeAdminSerializer(URLSafeImageMixin, serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = '__all__'

class EventAdminSerializer(URLSafeImageMixin, serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
