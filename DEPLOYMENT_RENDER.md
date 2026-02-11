# Deploying to Render (Manual Web Service)

This guide explains how to MANUALLY configure your Django project on **Render** as a Web Service.
Because we are using **SQLite**, you must carefully follow the instructions to set up a **Persistent Disk** and configure the commands correctly.

## Prerequisites
- A [Render](https://render.com/) account.
- Your project files ready (with `requirements.txt`, `build.sh`, and updated `settings.py`).
- **NO `render.yaml` file** (since we are doing this manually).

## Step 1: Push to GitHub/GitLab
Ensure your latest code is pushed to your repository.

## Step 2: Create a New Web Service
1.  Go to your Render Dashboard.
2.  Click **New +** -> **Web Service**.
3.  Connect your repository.

## Step 3: Configure the Web Service (CRITICAL)
Use the following settings exactly.

### Name & Runtime
-   **Name**: `joyceee` (or whatever you like)
-   **Runtime**: **Python 3**

### Build Command
-   **Value**: `./build.sh`
-   **IMPORTANT**: Do **NOT** put `python manage.py migrate` here. The build phase does not have access to the Persistent Disk, and your deployment will fail if you try to migrate here.

### Start Command
-   **Value**: `python manage.py migrate && gunicorn JOYCEEE.wsgi:application`
-   **Explanation**: This command runs `migrate` FIRST (to update the database), and THEN starts the server. This happens at **runtime**, when the disk is mounted.

### Instance Type
-   **Type**: **Starter** (or higher).
    > [!IMPORTANT]
    > **Free Tier Consideration**: The "Free" tier on Render *does not support Persistent Disks*. To use SQLite reliably, you typically need the **Team** or **Individual Paid** plan that supports disks.
    > If you are on the Free tier, your database will encompass a temporary filesystem and will be **deleted** every time the app deploys or restarts.

## Step 4: Environment Variables
Add the following Environment Variables in the "Environment" tab:

| Key | Value | Description |
| :--- | :--- | :--- |
| `DJANGO_SECRET_KEY` | `(generate a random key)` | Security key |
| `RENDER` | `true` | Tells settings.py to use the disk path |
| `PYTHON_VERSION` | `3.10.0` | Or your preferred version |

## Step 5: Add a Persistent Disk (REQUIRED for SQLite)
**If you skip this, your database will be deleted on every deploy.**

1.  Go to the **Disks** tab (or "Disks" section during creation).
2.  Click **Add Disk**.
3.  **Name**: `sqlite_data`
4.  **Mount Path**: `/var/data`
    -   *Why?* Our `settings.py` is configured to look for the DB at `/var/data/db.sqlite3` when the `RENDER` env var is present.
5.  **Size**: 1 GB.

## Step 6: Deploy
Click **Create Web Service**. Render will:
1.  Clone your repo.
2.  Run `./build.sh` (install deps, collect static).
3.  **Mount the Disk.**
4.  Run `Start Command` (Run migrations -> Start Gunicorn).

## Troubleshooting "Unable to open database file"
If you see `sqlite3.OperationalError: unable to open database file`, it means `migrate` ran before the disk was ready.
-   **Check Build Command**: Make sure it is JUST `./build.sh`.
-   **Check Start Command**: Make sure it starts with `python manage.py migrate`.
-   **Check Disk Mount**: Ensure the disk is mounted at `/var/data`.
