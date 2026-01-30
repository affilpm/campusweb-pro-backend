from django.contrib import admin
from .models import ClassCategory, Subject, AcademicsPage

@admin.register(ClassCategory)
class ClassCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'is_active')
    list_editable = ('order', 'is_active')

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    filter_horizontal = ('categories',)

@admin.register(AcademicsPage)
class AcademicsPageAdmin(admin.ModelAdmin):
    list_display = ('hero_title',)
