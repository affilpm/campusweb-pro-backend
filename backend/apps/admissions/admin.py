from django.contrib import admin
from .models import AdmissionSettings, AdmissionStep

@admin.register(AdmissionSettings)
class AdmissionSettingsAdmin(admin.ModelAdmin):
    list_display = ('hero_title', 'is_open')

@admin.register(AdmissionStep)
class AdmissionStepAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)
