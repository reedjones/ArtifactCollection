# Check if Git is installed

# Check if the number of arguments is correct
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <github-username> <repository-name>"
    exit 1
fi
export GH_USERNAME="$1"
export REPO_NAME="$2"


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
