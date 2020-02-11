from django.views.generic import TemplateView
from mydjango.celery import show_hello_world
from .models import DemoModel
from opentracing import global_tracer
# Create your views here.


class ShowHelloWorld(TemplateView):
    template_name = 'hello_world.html'

    def get(self, *args, **kwargs):
        with global_tracer().start_active_span('view_hello_world'):
            show_hello_world.apply_async()
        return super().get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['demo_content'] = DemoModel.objects.all()
        return context
