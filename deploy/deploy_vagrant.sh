#!/bin/bash
# This script represents the actions you'd perform on a remote server
# Check if GitHub CLI is installed
NGINX_CONF="/path/to/nginx/conf"
NGINX_SITE_ENABLED="/path/to/nginx/sites-enabled"
NGINX_SERVER_NAME="your-nginx-server-name"
GUNICORN_USER="your-gunicorn-user"
GUNICORN_GROUP="your-gunicorn-group"
GUNICORN_WORKING_DIRECTORY="$PROJECT_ROOT"
GUNICORN_WSGI_APPLICATION="your-wsgi-application"
SYSTEMCTL_SERVICE_NAME="your-systemctl-service-name"




# GitHub username and repository name
export GH_USERNAME="$1"
export REPO_NAME="$2"
CUR_DIR=$(pwd)
export PROJECT_ROOT="$CUR_DIR/$REPO_NAME"
export GH_USERNAME=GH_USERNAME
export REPO_NAME=REPO_NAME
export VIRTUAL_ENV=$PROJECT_ROOT/venv



if [ ! -d "$VIRTUAL_ENV" ]; then
    python -m venv "$VIRTUAL_ENV"
fi

if [ ! -d "$PROJECT_ROOT" ]; then
    mkdir "$PROJECT_ROOT"
    # Add any additional setup for the project directory if needed
fi

if ! grep -q "export PROJECT_ROOT" "$PROFILE_FILE"; then
    echo "export PROJECT_ROOT=\"$PROJECT_ROOT\"" >> "$PROFILE_FILE"
fi

if ! grep -q "export VIRTUAL_ENV" "$PROFILE_FILE"; then
    echo "export VIRTUAL_ENV=\"$VIRTUAL_ENV\"" >> "$PROFILE_FILE"
fi

if ! grep -q "export DJANGO_SECRET_KEY" "$PROFILE_FILE"; then
    echo "export DJANGO_SECRET_KEY=\"$DJANGO_SECRET_KEY\"" >> "$PROFILE_FILE"
fi

if ! grep -q "export APP_SETUP_DONE" "$PROFILE_FILE"; then
    echo "export NGINX_CONF=\"$NGINX_CONF\"" >> "$PROFILE_FILE"
    echo "export NGINX_SITE_ENABLED=\"$NGINX_SITE_ENABLED\"" >> "$PROFILE_FILE"
    echo "export NGINX_SERVER_NAME=\"$NGINX_SERVER_NAME\"" >> "$PROFILE_FILE"
    echo "export GUNICORN_USER=\"$GUNICORN_USER\"" >> "$PROFILE_FILE"
    echo "export GUNICORN_GROUP=\"$GUNICORN_GROUP\"" >> "$PROFILE_FILE"
    echo "export GUNICORN_WORKING_DIRECTORY=\"$GUNICORN_WORKING_DIRECTORY\"" >> "$PROFILE_FILE"
    echo "export GUNICORN_WSGI_APPLICATION=\"$GUNICORN_WSGI_APPLICATION\"" >> "$PROFILE_FILE"
    echo "export SYSTEMCTL_SERVICE_NAME=\"$SYSTEMCTL_SERVICE_NAME\"" >> "$PROFILE_FILE"
    echo "export APP_SETUP_DONE=1" >> "$PROFILE_FILE"
fi
# Additional environment variables





source "$VIRTUAL_ENV/bin/activate"


# Set up profile file if not exists
PROFILE_FILE="$HOME/.profile"
touch "$PROFILE_FILE"

# Check if the environment variables are already set in the profile file


source setup_env.sh # Sets up other env variables needed
source "$PROFILE_FILE"

sh ./setup_github GH_USERNAME REPO_NAME

source "$VIRTUAL_ENV"/bin/activate
export DJANGO_SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')





# Load environment variables


sh ./setup_systemctl.sh
sh ./setup_nginx.sh


cd $REPO_NAME || exit

# Runs final stage, migration, install requriments, etc..
bash deploy.sh
