# Run manage.py tasks
ssh "$DEPLOY_TARGET_USER@$DEPLOY_TARGET_IP" "cd $PROJECT_ROOT && python manage.py migrate && python manage.py collectstatic --noinput"
