if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <username> <target ip>"
    exit 1
fi

# Deploy target SSH details
DEPLOY_TARGET_USER="$1"
DEPLOY_TARGET_IP="$2"

# SSH to deploy target
ssh "$DEPLOY_TARGET_USER@$DEPLOY_TARGET_IP" 'echo "SSH connection to deploy target successful"'
