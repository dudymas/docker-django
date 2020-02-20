from django.views.generic import TemplateView
from mydjango.celery import show_hello_world
from .models import DemoModel
from .decorators import add_span, skip_django_trace

# Create your views here.


class ShowHelloWorld(TemplateView):
    template_name = 'hello_world.html'

    def get(self, *args, **kwargs):
        show_hello_world.apply_async()
        return super().get(*args, **kwargs)

    @add_span()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['demo_content'] = DemoModel.objects.all()
        return context


@skip_django_trace
class ShowUntracedHelloWorld(TemplateView):
    """ NOTE: the skip decorator only works on the view.
        the celery and psycopg stuff below will still show up!
    """
    template_name = 'hello_world.html'

    def get(self, *args, **kwargs):
        show_hello_world.apply_async()
        return super().get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['demo_content'] = DemoModel.objects.all()
        return context
