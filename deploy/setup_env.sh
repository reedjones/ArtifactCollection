#!/bin/bash

# Set up your project-specific environment variables

# Django-related variables
export DJANGO_SECRET_KEY="your_secret_key"
export DEBUG=True
export DATABASE_NAME="your_db_name"
export DATABASE_USER="your_db_user"
export DATABASE_PASSWORD="your_db_password"
export DATABASE_HOST="localhost"
export DATABASE_PORT="5432"

# Gunicorn-related variables
export GUNICORN_BIND_ADDRESS="127.0.0.1:8000"

# Other project-specific variables
export OTHER_VARIABLE="your_value"

export GH_USERNAME=reedjones
export REPO_NAME=artifactcollection


echo "Environment variables have been set up."
