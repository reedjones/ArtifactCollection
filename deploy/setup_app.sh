#!/bin/bash


# Change directory to your project
cd $PROJECT_ROOT || exit

# Pull the latest changes from the main branch
git pull --no-edit --no-rebase origin main

# Additional deployment steps...
export DEBUG=False

# Activate virtual environment if using one

# Install or update dependencies
pip install -r requirements.txt

# Automated backup
python manage.py dumpdata > backup.json

# Apply database migrations
python manage.py migrate

# Restart Gunicorn or your application server
systemctl restart gunicorn  # Replace with your actual command
systemctl restart nginx  # Corrected typo in 'nginx'

