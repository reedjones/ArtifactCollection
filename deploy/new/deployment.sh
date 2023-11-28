#!/bin/bash

# Deploy target SSH details
DEPLOY_TARGET_USER="user"
DEPLOY_TARGET_IP="deploy-target-ip"
DJANGO_SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')


# Set up project-specific details
export DJANGO_SECRET_KEY="your_secret_key"
export PROJECT_ROOT="/path/to/your/project"

# Check if SSH key pair exists
if [ ! -f "$HOME/.ssh/id_rsa" ]; then
    # Generate SSH key pair
    ssh-keygen -t rsa -b 4096 -C "your_email@example.com" -f "$HOME/.ssh/id_rsa" -N ""
fi

# Test SSH connection to the deploy target
ssh -o BatchMode=yes -o ConnectTimeout=5 "$DEPLOY_TARGET_USER@$DEPLOY_TARGET_IP" 'echo "SSH Connection Successful"'
if [ $? -ne 0 ]; then
    echo "SSH connection to deploy target failed. Exiting script."
    exit 1
fi

# SSH to deploy target
ssh "$DEPLOY_TARGET_USER@$DEPLOY_TARGET_IP" 'echo "SSH connection to deploy target successful"'

# Set up environment variables on the deploy target
ssh "$DEPLOY_TARGET_USER@$DEPLOY_TARGET_IP" "
    export DJANGO_SECRET_KEY=\"$DJANGO_SECRET_KEY\"
    export PROJECT_ROOT=\"$PROJECT_ROOT"
    # Add other environment variables as needed
"

# Check if systemctl service exists
if ! ssh "$DEPLOY_TARGET_USER@$DEPLOY_TARGET_IP" systemctl is-active --quiet your-service-name; then
    echo "Systemctl service not found. Setting up..."
    # Set up your systemctl service
    # ...
    # Restart the service
    ssh "$DEPLOY_TARGET_USER@$DEPLOY_TARGET_IP" sudo systemctl restart your-service-name
else
    echo "Systemctl service already exists."
fi

# Check if Nginx is installed
ssh "$DEPLOY_TARGET_USER@$DEPLOY_TARGET_IP" 'nginx -v'
if [ $? -ne 0 ]; then
    echo "Nginx not found. Installing..."
    # Install Nginx
    ssh "$DEPLOY_TARGET_USER@$DEPLOY_TARGET_IP" 'sudo apt-get install nginx -y'
    # Start Nginx
    ssh "$DEPLOY_TARGET_USER@$DEPLOY_TARGET_IP" 'sudo systemctl start nginx'
else
    echo "Nginx already installed."
fi

# Check if the project directory exists
if ! ssh "$DEPLOY_TARGET_USER@$DEPLOY_TARGET_IP" [ -d "$PROJECT_ROOT" ]; then
    echo "Project directory not found. Creating..."
    # Create project directory
    ssh "$DEPLOY_TARGET_USER@$DEPLOY_TARGET_IP" "mkdir -p $PROJECT_ROOT"
else
    echo "Project directory already exists."
fi

# Change to the project directory
ssh "$DEPLOY_TARGET_USER@$DEPLOY_TARGET_IP" "cd $PROJECT_ROOT || exit"

# Check if Git is installed
ssh "$DEPLOY_TARGET_USER@$DEPLOY_TARGET_IP" 'git --version'
if [ $? -ne 0 ]; then
    echo "Git not found. Installing..."
    # Install Git
    ssh "$DEPLOY_TARGET_USER@$DEPLOY_TARGET_IP" 'sudo apt-get install git -y'
else
    echo "Git already installed."
fi

# Check if the Git repository is initialized
if ! ssh "$DEPLOY_TARGET_USER@$DEPLOY_TARGET_IP" [ -d "$PROJECT_ROOT/.git" ]; then
    echo "Git repository not found. Initializing..."
    # Initialize Git repository
    ssh "$DEPLOY_TARGET_USER@$DEPLOY_TARGET_IP" "cd $PROJECT_ROOT && git init"
fi

# Pull the latest changes from the main branch
ssh "$DEPLOY_TARGET_USER@$DEPLOY_TARGET_IP" "cd $PROJECT_ROOT && git pull origin main"

# Run manage.py tasks
ssh "$DEPLOY_TARGET_USER@$DEPLOY_TARGET_IP" "cd $PROJECT_ROOT && python manage.py migrate && python manage.py collectstatic --noinput"

# Restart Systemctl services
ssh "$DEPLOY_TARGET_USER@$DEPLOY_TARGET_IP" "sudo systemctl restart your-service-name"

echo "Deployment script completed successfully."
