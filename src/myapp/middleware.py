from opentracing_instrumentation.client_hooks import install_all_patches
from django_opentracing import OpenTracingMiddleware

class MyTraceMiddleware(OpenTracingMiddleware):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if hasattr(view_func.view_class, '__skip_trace__'):
            return None
        return super().process_view(request, view_func, view_args, view_kwargs)

class MyMiddleware(object):
    def __init__(self, get_response):
        install_all_patches()
        self.get_response = get_response
    
    def __call__(self, request):
        return self.get_response(request)