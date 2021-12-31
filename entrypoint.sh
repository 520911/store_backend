 #!/bin/bash
python manage.py migrate

# Start server
echo "Starting server"
python manage.py runserver 0.0.0.0:8000
celery -A shop woker -l info