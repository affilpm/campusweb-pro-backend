from django.contrib import admin
from .models import Notice, Event

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'publish_date', 'status', 'is_important')
    list_filter = ('status', 'is_important', 'publish_date')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_date', 'status', 'is_featured')
    list_filter = ('status', 'is_featured', 'event_date')
    search_fields = ('title', 'excerpt')
    prepopulated_fields = {'slug': ('title',)}
