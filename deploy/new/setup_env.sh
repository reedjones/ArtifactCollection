# Set up environment variables on the deploy target
ssh "$DEPLOY_TARGET_USER@$DEPLOY_TARGET_IP" '
    export DJANGO_SECRET_KEY="your_secret_key"
    export PROJECT_ROOT="/path/to/your/project"
    # Add other environment variables as needed
'
