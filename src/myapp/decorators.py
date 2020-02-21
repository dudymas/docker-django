from opentracing import global_tracer


class add_span(object):
    """given an existing trace, add more context. Accepts a 'name' param otherwise uses function name"""
    def __init__(self, name=None):
        self.name = name
    def __call__(self, func):
        deco_self = self
        def wrapper(*args, **kwargs):
            name = deco_self.name
            if not name:
                name = func.__name__
            print(func.__class__)
            print(func.__class__.__dict__.keys())
            tracer = global_tracer()
            if tracer.active_span:
                with tracer.start_active_span(name, child_of=tracer.active_span):
                    result = func(*args, **kwargs)
                    return result
            elif tracer.scope_manager.active:
                with tracer.start_active_span(name, child_of=tracer.scope_manager.active):
                    result = func(*args, **kwargs)
                    return result
        return wrapper


def skip_django_trace(func):
    """disable tracing on a django view function"""
    func.__skip_trace__ = True
    return func