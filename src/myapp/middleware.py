from opentracing_instrumentation.client_hooks import install_all_patches


class MyMiddleware(object):
    def __init__(self, get_response):
        install_all_patches()
        self.get_response = get_response
    
    def __call__(self, request):
        return self.get_response(request)