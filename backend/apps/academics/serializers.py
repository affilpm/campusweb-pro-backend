from rest_framework import serializers
from apps.core.serializers import URLSafeImageMixin

from .models import AcademicsPage, ClassCategory, Subject

class ClassCategoryPublicSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = ClassCategory
        fields = ['id', 'name', 'description', 'classes_range', 'image', 'order']
        
    def get_image(self, obj):
        if obj.image:
            return obj.image.url
        return None

class SubjectPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name', 'description', 'icon', 'is_core', 'order']

class AcademicsPagePublicSerializer(serializers.ModelSerializer):
    hero_image = serializers.SerializerMethodField()
    curriculum_image = serializers.SerializerMethodField()
    calendar_file = serializers.SerializerMethodField()
    
    class Meta:
        model = AcademicsPage
        exclude = ['created_at', 'updated_at']
        
    def get_hero_image(self, obj):
        if obj.hero_image:
            return obj.hero_image.url
        return None

    def get_curriculum_image(self, obj):
        if obj.curriculum_image:
            return obj.curriculum_image.url
        return None

    def get_calendar_file(self, obj):
        if obj.calendar_file:
            return obj.calendar_file.url
        return None

# Admin Serializers
class AcademicsPageAdminSerializer(URLSafeImageMixin, serializers.ModelSerializer):
    class Meta:
        model = AcademicsPage
        fields = '__all__'

class ClassCategoryAdminSerializer(URLSafeImageMixin, serializers.ModelSerializer):
    class Meta:
        model = ClassCategory
        fields = '__all__'

class SubjectAdminSerializer(URLSafeImageMixin, serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'
