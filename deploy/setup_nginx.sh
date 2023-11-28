#!/bin/bash

#!/bin/bash

# Check if Nginx setup is necessary
if [ ! -f "$NGINX_CONF" ] || [ ! -d "$NGINX_SITE_ENABLED" ]; then
    echo "Nginx setup is necessary. Proceeding with setup..."

    # ... (Nginx setup steps)
    # Set a flag indicating Nginx setup is done
# Create an Nginx server block configuration file
    sudo tee "$NGINX_CONF" > /dev/null <<EOL
    server {
        listen 80;
        server_name your-domain.com;  # Replace with your actual domain

        location = /favicon.ico { access_log off; log_not_found off; }
        location /static/ {
            root $PROJECT_ROOT;
        }

        location / {
            include proxy_params;
            proxy_pass http://127.0.0.1:8000;  # Assuming Gunicorn is running on this address and port
        }
    }
EOL

# Create a symbolic link to enable the Nginx site
    sudo ln -s "$NGINX_CONF" "$NGINX_SITE_ENABLED"

    # Test Nginx configuration
    sudo nginx -t

    # Reload Nginx to apply changes
    sudo systemctl reload nginx
    echo "export NGINX_SETUP_DONE=1" >> "$PROFILE_FILE"


    echo "Nginx has been set up!"


else
    echo "Nginx setup has already been done. No need to proceed."
fi