# Restart Systemctl services
ssh "$DEPLOY_TARGET_USER@$DEPLOY_TARGET_IP" "sudo systemctl restart your-service-name"
