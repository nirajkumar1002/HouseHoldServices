celery -A app.celery_app beat -l INFO
~/go/bin/MailHog
celery -A app.celery_app worker -l INFO
redis-server

#start celery worker before beats