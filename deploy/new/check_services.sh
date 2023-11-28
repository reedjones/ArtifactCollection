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
