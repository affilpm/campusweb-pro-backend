# How to Reset a Database Table on DigitalOcean Droplet

If you need to reset a specific table because of a schema change or error, follow these steps.

## Option 1: Re-run Migrations (Safest)
This attempts to reverse the migrations for the specific app and re-apply them.

1.  **SSH into your Droplet:**
    ```bash
    ssh root@your_droplet_ip
    ```

2.  **Navigate to your project directory:**
    ```bash
    cd /path/to/your/project
    ```

3.  **Run the migrate command to revert:**
    Replace `school_info` with the name of the app containing the table you want to reset.
    ```bash
    docker-compose exec web python manage.py migrate school_info zero
    ```

4.  **Re-apply migrations:**
    ```bash
    docker-compose exec web python manage.py migrate school_info
    ```

## Option 2: Force Drop Table (If Option 1 fails)
If the migration history is broken, you may need to manually drop the table.

1.  **Access the Database Container:**
    ```bash
    docker-compose exec db psql -U postgres -d school_db
    ```

2.  **Drop the Table:**
    Find the exact table name (usually `appname_modelname`, e.g., `school_info_managementmember`).
    ```sql
    \dt  -- List all tables to find the name
    DROP TABLE school_info_managementmember CASCADE;
    ```

3.  **Clean Migration History (Optional but recommended if syncing issues):**
    ```sql
    DELETE FROM django_migrations WHERE app='school_info';
    ```
    *Note: Be careful with this. Only do it if you plan to fake-apply the initial migrations or if you are resetting the app entirely.*

4.  **Exit SQL Prompt:**
    ```sql
    \q
    ```

5.  **Re-run Migrations:**
    ```bash
    docker-compose exec web python manage.py migrate
    ```
    If you cleared the migration history, you might need:
    ```bash
    docker-compose exec web python manage.py migrate --fake-initial
    ```

## Option 3: Reset Entire Database (Destructive)
**Warning: This deletes ALL data.**

```bash
docker-compose exec web python manage.py flush --no-input
```

Then load your backup if needed:
```bash
docker-compose exec web python manage.py loaddata db_backup_latest.json
```
