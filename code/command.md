## for the backend part
> cd code/backend
* install all requirements from requirements.text
* run the backend
  > python3 app.py
## for the frontend part
> cd code/frontend
* install node modules
   > npm i
* run the frontend
   > npm run serve
   
## for Backend jobs
* Starts the Celery beat scheduler to schedule and dispatch periodic tasks.
  > celery -A app.celery_app beat -l INFO
* Runs MailHog, a tool to capture and test emails sent by an application in a local testing environment.
  >  ~/go/bin/MailHog
* Starts a Celery worker to process queued tasks.
  > celery -A app.celery_app worker -l INFO
* Starts the Redis server, which acts as a message broker for Celery and a data store for caching.
  > redis-server

#start celery worker before beats
