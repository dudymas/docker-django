from django.apps import AppConfig
from mydjango import settings
from jaeger_client import Config
from myapp.signals import connect_celery_signals


def init_jaeger_tracer(service_name='mydjango'):
    config = Config(
        config={
            'sampler': {'type': 'const', 'param': 1,},
            'logging': True,
            'local_agent': {'reporting_host': 'jaeger', 'reporting_port': '6831',},
        },
        service_name=service_name,
        validate=True,
    )
    return config.initialize_tracer()


class MyappConfig(AppConfig):
    name = 'myapp'

    def __init__(self, app_name, app_module):
        if not settings.IS_CELERY_WORKER:
            init_jaeger_tracer()
        connect_celery_signals()
        super().__init__(app_name, app_module)
