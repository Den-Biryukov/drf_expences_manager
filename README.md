## DRF API expense manager

### For start celery-beat run in different terminals:

    -python manage.py runserver

    -docker run -p 127.0.0.1:6379:6379 --name celery-send-em --rm -d redis

    -celery -A drf_expences_manager worker -l info

    -celery -A drf_expences_manager beat -l info

