
from __future__ import absolute_import
import os
from celery import Celery
from django.apps import apps, AppConfig
from django.conf import settings



if not settings.configured:
    # set the default Django settings module for the 'celery' program.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')  # pragma: no cover


app = Celery('cacaosms', broker='redis://localhost:6379/0')


class CeleryConfig(AppConfig):
    name = 'cacaosms.taskapp'
    verbose_name = 'Celery Config'

    def ready(self):
        # Using a string here means the worker will not have to
        # pickle the object when using Windows.
        app.config_from_object('django.conf:settings', namespace='CELERY')
        #installed_apps = [app_config.name for app_config in apps.get_app_configs()]
        #app.autodiscover_tasks(lambda: installed_apps, force=True)
        app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))  # pragma: no cover

@app.task
def add(x, y):
    return x + y


from cacaosms.backends import send_sms

@app.task
def send_sms_task(phone_number_to, message, from_str=None, to_str=None, id_str=None):
    send_sms(phone_number_to, message, from_str, to_str, id_str)
