# Check if SSH key pair exists
if [ ! -f "$HOME/.ssh/id_rsa" ]; then
    # Generate SSH key pair
    ssh-keygen -t rsa -b 4096 -C "reedjones760@yahoo.com" -f "$HOME/.ssh/id_rsa" -N ""
fi

# Test SSH connection to the deploy target
ssh -o BatchMode=yes -o ConnectTimeout=5 user@deploy-target 'echo "SSH Connection Successful"'
if [ $? -ne 0 ]; then
    echo "SSH connection to deploy target failed. Exiting script."
    exit 1
fi
