import os

apps = [
    'admissions',
    'academics',
    'communication',
    'gallery',
    'school_info',
    'landing'
]

base_dir = 'backend/apps'

for app in apps:
    urls_content = f"""from django.urls import path
from rest_framework.routers import DefaultRouter
# from .views import {app.capitalize()}ViewSet # Placeholder

router = DefaultRouter()
# router.register(r'', {app.capitalize()}ViewSet)

urlpatterns = [
    # path('', include(router.urls)),
]
"""
    with open(os.path.join(base_dir, app, 'urls.py'), 'w') as f:
        f.write(urls_content)
