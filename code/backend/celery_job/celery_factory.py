

from celery import Celery, Task
from flask import Flask

class CeleryConfig():
    broker_url = "redis://localhost:6379/0"
    result_backend = "redis://localhost:6379/1"
    timezone= "Asia/Kolkata"
    broker_connection_retry_on_startup= True

#taking a flask application and returning a cerely instance
def make_celery(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(CeleryConfig)
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app


