from __future__ import absolute_import, unicode_literals

import logging
from datetime import date

from celery import shared_task
from django.apps import apps
from django.conf import settings

from mydjango.celery import app

logger = logging.getLogger("celery")


@shared_task(bind=True)
def show_hello_world(self):
    from .models import DemoModel
    model = DemoModel.objects.first()
    model.body = date.today()
    model.save()
    print('finished updating demo model')
