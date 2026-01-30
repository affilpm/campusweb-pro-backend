from django.contrib import admin
from .models import HeroSection, HomeAboutSection, AcademicHighlight

@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'id')

@admin.register(HomeAboutSection)
class HomeAboutSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'established_year', 'id')

@admin.register(AcademicHighlight)
class AcademicHighlightAdmin(admin.ModelAdmin):
    list_display = ('title', 'value', 'order')
    list_editable = ('order',)
