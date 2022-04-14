from django.db import models

from flowly.constants.models import FieldLength


class Run(models.Model):
    identity = models.CharField(max_length=FieldLength.UUID, unique=True)
    method = models.CharField(max_length=FieldLength.IDENTITY)
    started = models.DateTimeField(auto_now_add=True)
    completed = models.DateTimeField(null=True)


class RunState(models.Model):
    identity = models.CharField(max_length=FieldLength.UUID, unique=True)
    data = models.JSONField()
    run = models.ForeignKey(Run, on_delete=models.PROTECT)
    node = models.CharField(max_length=FieldLength.NAME, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
