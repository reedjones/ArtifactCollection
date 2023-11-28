#!/bin/bash

# Replace these variables with your actual values
PROJECT_ROOT="/path/to/your/project"
VENV_PATH="/path/to/your/virtualenv"

# Install Gunicorn using your virtual environment
$VENV_PATH/bin/pip install gunicorn

# Create a Gunicorn systemd service file
sudo tee "/etc/systemd/system/gunicorn.service" > /dev/null <<EOL
[Unit]
Description=gunicorn daemon for your-project
After=network.target

[Service]
User=your-username
Group=your-groupname
WorkingDirectory=$PROJECT_ROOT
ExecStart=$VENV_PATH/bin/gunicorn your_project.wsgi:application -b 127.0.0.1:8000
Restart=always

[Install]
WantedBy=multi-user.target
EOL

# Reload systemd to read the new service file
sudo systemctl daemon-reload

# Enable the Gunicorn service to start on boot
sudo systemctl enable gunicorn

# Start the Gunicorn service
sudo systemctl start gunicorn

echo "Gunicorn has been set up and started!"
