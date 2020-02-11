from __future__ import absolute_import, unicode_literals
import os, time
from celery import Celery, shared_task
import logging
logger = logging.getLogger("Celery")
from opentracing import global_tracer

from myapp.apps import init_jaeger_tracer
from myapp.signals import connect_celery_signals
from celery.signals import worker_process_init
from opentracing_instrumentation.client_hooks import install_all_patches

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mydjango.settings')

app = Celery('mydjango')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(['mydjango'])

@worker_process_init.connect
def hook_up_dat_trace_baybay(*args, **kwargs):
    init_jaeger_tracer()
    connect_celery_signals()
    install_all_patches()


@shared_task
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


@shared_task(bind=True)
def show_hello_world(self):
    logger.info("-"*25)
    logger.info("Printing Hello from Celery")
    logger.info("-"*25)
