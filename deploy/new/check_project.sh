# Check if the project directory exists
if ! ssh "$DEPLOY_TARGET_USER@$DEPLOY_TARGET_IP" [ -d "$PROJECT_ROOT" ]; then
    echo "Project directory not found. Creating..."
    # Create project directory
    ssh "$DEPLOY_TARGET_USER@$DEPLOY_TARGET_IP" "mkdir -p $PROJECT_ROOT"
else
    echo "Project directory already exists."
fi
