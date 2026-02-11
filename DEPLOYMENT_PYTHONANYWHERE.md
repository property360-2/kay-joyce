# Deploying to PythonAnywhere

This guide will help you host your Django project on PythonAnywhere using SQLite.

## Prerequisites
- A PythonAnywhere account (Beginner account is fine).
- Your project files ready (which they are!).

## Step 1: Upload Your Code

### Option A: Using GitHub (Recommended)
1.  Push your code to GitHub.
2.  Open a **Bash Console** on PythonAnywhere.
3.  Clone your repository:
    ```bash
    git clone https://github.com/yourusername/your-repo.git
    ```

### Option B: Uploading a Zip
1.  Zip your `JOYCEEE` folder (the one containing `manage.py`).
2.  Go to the **Files** tab on PythonAnywhere.
3.  Upload the zip file.
4.  Open a **Bash Console** and unzip it:
    ```bash
    unzip JOYCEEE.zip
    ```

## Step 2: Set Up Virtual Environment

In the PythonAnywhere **Bash Console**:

```bash
# Change to your project directory
cd ~/JOYCEEE  # or whatever your folder is named

# Create a virtual environment
python3 -m venv myvenv

# Activate it
source myvenv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Step 3: Configure Web App

1.  Go to the **Web** tab on PythonAnywhere.
2.  **Add a new web app**.
3.  Select **Manual Configuration** (select Python 3.10 or newer).
    -   *Note: Do not select the "Django" wizard, as manual gives you more control over the virtualenv.*

### Virtualenv
-   In the **Virtualenv** section, enter the path to your virtualenv:
    `/home/yourusername/JOYCEEE/myvenv`
    (Replace `yourusername` with your actual PythonAnywhere username).

### WSGI Configuration File
-   Click the link to edit the **WSGI configuration file**.
-   Delete the default content and paste this (adjust paths as needed):

```python
import os
import sys

# Add your project directory to the sys.path
path = '/home/yourusername/JOYCEEE'  # <-- UPDATE THIS PATH
if path not in sys.path:
    sys.path.append(path)

# Set environment variables
os.environ['DJANGO_SETTINGS_MODULE'] = 'JOYCEEE.settings'
os.environ['DJANGO_SECRET_KEY'] = 'your-secret-key-here' # <-- CHANGE THIS
os.environ['DJANGO_DEBUG'] = 'False'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

## Step 4: Static Files

1.  In the **Bash Console**, run:
    ```bash
    python manage.py collectstatic
    ```
    This will create a `staticfiles` folder in your project directory.

2.  In the **Web** tab, scroll to **Static Files**.
3.  Add a new mapping:
    -   **URL**: `/static/`
    -   **Directory**: `/home/yourusername/JOYCEEE/staticfiles`

## Step 5: Database

Since we are using SQLite, the database is a file (`db.sqlite3`).

1.  In the **Bash Console**, make sure migrations are applied:
    ```bash
    python manage.py migrate
    ```

## Step 6: Reload

1.  Go to the **Web** tab.
2.  Click the big green **Reload** button.
3.  Click the link to your site (e.g., `yourusername.pythonanywhere.com`).

## Troubleshooting

-   **Files not found?** Check your paths in the WSGI file and Static Files section.
-   **Server Error (500)?** Check the **Error Log** in the Web tab.
