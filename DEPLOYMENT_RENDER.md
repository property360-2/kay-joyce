# Deploying to Render (Web Service with SQLite)

This guide explains how to host your Django project on **Render** as a Web Service.
Because we are using **SQLite**, we must use a **Persistent Disk** to prevent data loss when the app restarts.

## Prerequisites
- A [Render](https://render.com/) account.
- Your project files ready (with `requirements.txt`, `build.sh`, and updated `settings.py`).

## Step 1: Push to GitHub/GitLab
Ensure your latest code is pushed to your repository.

## Step 2: Create a New Web Service
1.  Go to your Render Dashboard.
2.  Click **New +** -> **Web Service**.
3.  Connect your repository.

## Step 3: Configure the Web Service
Use the following settings:

-   **Name**: `joyceee` (or whatever you like)
-   **Runtime**: **Python 3**
-   **Build Command**: `./build.sh`
-   **Start Command**: `gunicorn JOYCEEE.wsgi:application`
-   **Instance Type**: **Starter** (or higher).
    > [!IMPORTANT]
    > **Free Tier Consideration**: The "Free" tier on Render *does not support Persistent Disks*. To use SQLite reliably, you typically need the **Team** or **Individual Paid** plan that supports disks, OR you can use Render's managed PostgreSQL (which is often free/cheap).
    > **However, since you requested SQLite**, you MUST check if your plan supports "Disks". If not, your database will reset every time the app deploys or sleeps.

## Step 4: Environment Variables
Add the following Environment Variables in the "Environment" tab:

| Key | Value | Description |
| :--- | :--- | :--- |
| `DJANGO_SECRET_KEY` | `(generate a random key)` | Security key |
| `RENDER` | `true` | Tells settings.py to use the disk path |
| `PYTHON_VERSION` | `3.10.0` | Or your preferred version |

## Step 5: Add a Persistent Disk (CRITICAL)
**If you skip this, your database will be deleted on every deploy.**

1.  Go to the **Disks** tab (or "Disks" section during creation).
2.  Click **Add Disk**.
3.  **Name**: `sqlite_data`
4.  **Mount Path**: `/var/data`
    -   *Why?* Our `settings.py` is configured to look for the DB at `/var/data/db.sqlite3` when the `RENDER` env var is present.
5.  **Size**: 1 GB (should be enough).

## Step 6: Deploy
Click **Create Web Service**. Render will:
1.  Clone your repo.
2.  Run `./build.sh` (install deps, collect static, migrate).
3.  Start Gunicorn.

## Troubleshooting
-   **Database is empty/resetting?** Check if you added the Persistent Disk and mounted it to `/var/data`.
-   **Build failed?** Check the logs. Ensure `build.sh` is executable (Render usually handles this, but you can `chmod +x build.sh` locally and push if needed).
