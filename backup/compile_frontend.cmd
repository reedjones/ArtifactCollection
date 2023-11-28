npm run build
python manage.py collectstatic --noinput
npx webpack --config webpack.config.js --watch

