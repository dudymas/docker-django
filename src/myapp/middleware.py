from django_opentracing import OpenTracingMiddleware
from opentracing_instrumentation.client_hooks import celery as oi_celery
from opentracing_instrumentation.client_hooks import psycopg2 as oi_psycopg2
from opentracing_instrumentation.client_hooks import requests as oi_requests
from opentracing_instrumentation.client_hooks import strict_redis as oi_strict_redis
from opentracing_instrumentation.client_hooks import urllib as oi_urllib
from opentracing_instrumentation.client_hooks import urllib2 as oi_urllib2


class MyTraceMiddleware(OpenTracingMiddleware):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if hasattr(view_func, 'view_class') and hasattr(view_func.view_class, '__skip_trace__'):
            return None
        return super().process_view(request, view_func, view_args, view_kwargs)


class MyMiddleware(object):
    def __init__(self, get_response):
        oi_celery.install_patches()
        oi_psycopg2.install_patches()
        oi_strict_redis.install_patches()
        oi_urllib.install_patches()
        oi_urllib2.install_patches()
        oi_requests.install_patches()
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)
