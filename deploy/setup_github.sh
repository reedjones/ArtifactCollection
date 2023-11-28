#!/bin/bash


if ! command -v gh &> /dev/null; then
    echo "GitHub CLI (gh) is not installed. Please install it first."
    exit 1
fi

# Check if the number of arguments is correct
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <github-username> <repository-name>"
    exit 1
fi


if [ -d "$REPO_NAME" ]; then
    echo "Error: The directory '$REPO_NAME' already exists. Please choose a different directory name."
    exit 1
fi
#mkdir $REPO_NAME && cd $REPO_NAME

# Clone the existing repository to your local machine
git clone https://github.com/$GH_USERNAME/$EXISTING_REPO_NAME.git

echo "GitHub repository has been set up successfully!"