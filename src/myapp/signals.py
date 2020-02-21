import time
from celery.signals import before_task_publish, task_prerun, after_task_publish, task_postrun
from opentracing import global_tracer, Format


def inject_tracing_data(
    body, exchange, routing_key, headers, properties, declare, retry_policy, **kwargs
):
    tracer = global_tracer()
    scope = tracer.start_active_span('task_publish', finish_on_close=False)
    span_map = {}
    tracer.inject(scope.span, Format.HTTP_HEADERS, span_map)
    headers['span_map'] = span_map


def extract_tracing_data(sender=None, task_id=None, task=None, **kwargs):
    tracer = global_tracer()
    print(f'starting {task.name}')
    if hasattr(task.request, 'span_map'):
        ctxt = tracer.extract(Format.HTTP_HEADERS, task.request.span_map)
    if ctxt:
        print(f'using existing span, {ctxt}')
        tracer.start_active_span(task.name, child_of=ctxt, finish_on_close=False)
    else:
        print('making a new span!')
        tracer.start_active_span(task.name, finish_on_close=False)


def finish_trace(*args, **kwargs):
    tracer = global_tracer()
    if tracer.scope_manager.active:
        tracer.scope_manager.active.close()


def connect_celery_signals():
    before_task_publish.connect(inject_tracing_data)
    after_task_publish.connect(finish_trace)
    task_prerun.connect(extract_tracing_data)
    task_postrun.connect(finish_trace)
