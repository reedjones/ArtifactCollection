# Pull the latest changes from the main branch
ssh "$DEPLOY_TARGET_USER@$DEPLOY_TARGET_IP" "cd $PROJECT_ROOT && git pull origin main"
