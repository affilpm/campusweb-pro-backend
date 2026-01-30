# How to Reset Database in Droplet

Run these commands inside your Droplet to reset the database (delete all data) and start fresh:

**Note**: If `docker-compose` (with hyphen) is not found, use `docker compose` (with space).

1.  **Stop containers and delete volume**:
    ```bash
    docker compose down -v
    ```
    *(The `-v` flag is critical—it deletes the data volume)*

2.  **Get latest code**:
    ```bash
    git pull origin main
    ```

3.  **Rebuild and Start**:
    ```bash
    docker compose up -d --build
    ```
