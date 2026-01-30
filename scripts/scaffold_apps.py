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
    app_config_content = f"""from django.apps import AppConfig

class {app.capitalize()}Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.{app}'
"""
    with open(os.path.join(base_dir, app, 'apps.py'), 'w') as f:
        f.write(app_config_content)
