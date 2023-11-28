#!/bin/bash
# deploy.sh

export SECRET_KEY='your_secret_key'
export DEBUG=False

# Activate virtual environment if using one
source /path/to/venv/bin/activate

# Install or update dependencies
pip install -r requirements.txt

# Automated backup
python manage.py dumpdata > backup.json

# Apply database migrations

python manage.py migrate


# Restart Gunicorn or your application server
systemctl restart gunicorn  # Replace with your actual command
systemctl restart ngnix
# Additional steps as needed