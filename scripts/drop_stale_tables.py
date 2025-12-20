import os
import sys
import django
from django.db import connection

# Setup Django environment
sys.path.append(os.path.join(os.path.dirname(__file__), '../backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def drop_tables():
    with connection.cursor() as cursor:
        # Get all table names
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
        tables = [row[0] for row in cursor.fetchall()]

        # Filter tables to drop (content app and old feature apps)
        prefixes = [
            'content_', 
            'schools_', 'notices_', 'events_', 'gallery_', 'facilities_', 
            'achievements_', 'testimonials_', 'downloads_', 'academics_', 
            'admissions_', 'about_', 'public_disclosure_', 'seo_', 'contact_'
        ]
        
        tables_to_drop = [t for t in tables if any(t.startswith(p) for p in prefixes)]
        
        if not tables_to_drop:
            print("No stale tables found to drop.")
            return

        print(f"Dropping {len(tables_to_drop)} tables: {', '.join(tables_to_drop)}")
        
        # Drop tables with CASCADE to handle foreign keys
        for table in tables_to_drop:
            try:
                cursor.execute(f'DROP TABLE IF EXISTS "{table}" CASCADE')
                print(f"Dropped {table}")
            except Exception as e:
                print(f"Error dropping {table}: {e}")

if __name__ == "__main__":
    drop_tables()
