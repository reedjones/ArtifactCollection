#!/bin/bash

# Replace these variables with your actual values
# Check if systemctl setup is necessary
if ! systemctl is-active --quiet "$SYSTEMCTL_SERVICE_NAME"; then
    echo "Systemctl setup is necessary. Proceeding with setup..."

    # ... (Systemctl setup steps)

    # Create a systemd service file
    sudo tee "/etc/systemd/system/$SERVICE_NAME.service" > /dev/null <<EOL
        [Unit]
        Description=$SERVICE_NAME
        After=network.target

        [Service]
        User=your-username
        WorkingDirectory=$PROJECT_ROOT
        ExecStart=$VENV_PATH/bin/gunicorn your_project.wsgi:application -b 127.0.0.1:8000
        Restart=always

        [Install]
        WantedBy=multi-user.target
EOL

    # Reload systemd to read the new service file
    sudo systemctl daemon-reload

    # Enable the service to start on boot
    sudo systemctl enable $SERVICE_NAME

    # Start the service
    sudo systemctl start $SERVICE_NAME

    echo "Systemd service has been set up and started!"


    # Set a flag indicating Systemctl setup is done
    echo "export SYSTEMCTL_SETUP_DONE=1" >> "$PROFILE_FILE"

else
    echo "Systemctl setup has already been done. No need to proceed."
fi