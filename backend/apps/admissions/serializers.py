from rest_framework import serializers
from apps.core.serializers import URLSafeImageMixin

from .models import AdmissionSettings, AdmissionStep

class AdmissionStepAdminSerializer(URLSafeImageMixin, serializers.ModelSerializer):
    class Meta:
        model = AdmissionStep
        fields = '__all__'

class AdmissionStepPublicSerializer(serializers.ModelSerializer):
    step_number = serializers.IntegerField(source='order')
    
    class Meta:
        model = AdmissionStep
        fields = ['step_number', 'title', 'description']

class AdmissionSettingsPublicSerializer(serializers.ModelSerializer):
    steps = serializers.SerializerMethodField()
    
    def get_steps(self, obj):
        from .models import AdmissionStep
        steps = AdmissionStep.objects.all().order_by('order')
        return AdmissionStepPublicSerializer(steps, many=True).data
    
    class Meta:
        model = AdmissionSettings
        fields = [
            'hero_title', 'hero_subtitle', 'is_open', 'application_form_link',
            'overview_title', 'overview_content',
            'eligibility_title', 'eligibility_content',
            'documents_required', 'contact_info',
            'steps'
        ]


class AdmissionSettingsAdminSerializer(URLSafeImageMixin, serializers.ModelSerializer):
    class Meta:
        model = AdmissionSettings
        fields = '__all__'

