from django.views.generic import TemplateView
from myapp.tasks import show_hello_world
from .models import DemoModel
from .decorators import add_span, skip_django_trace
from datetime import date
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

# Create your views here.

from rest_framework import serializers


class DemoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DemoModel
        fields = ['title']

class DemoViewSet(ModelViewSet):
    queryset = DemoModel.objects.all()
    serializer_class = DemoSerializer


class ShowHelloWorld(TemplateView):
    template_name = 'hello_world.html'

    def get(self, *args, **kwargs):
        show_hello_world.apply_async()
        return super().get(*args, **kwargs)

    @add_span(name='update_demo_models')
    @action(methods='POST', detail=True)
    def update_model(self, *args, **kwargs):
        return Response(status=status.HTTP_200_OK)

    @add_span(name='ShowHelloWorld.get_context_data')
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
