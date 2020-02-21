from django.db import models
from myapp.decorators import add_span


class DemoModel(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()

    def __str__(self):
        return self.title

    @add_span(name='DemoModel.save')
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        return super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)