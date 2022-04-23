import datetime

from django.db import models

from flowly.constants.models import FieldLength
from flowly.decorators import flowly_material
from flowly.models.mixin import MaterialMixin



# When a model is decorated, it becomes addressable as:
#   namespace_name::unique_id

# NB: model instances are **only** accessed by the namespace indicated
# If a model should be accessed by more than one namespace, use multiple decorators
@flowly_material('flowly.tests.content_root.sales')
class Customer(MaterialMixin, models.Model):
    barcode_prefix = 'CUST'
    barcode_field_name = 'unique_id'
    unique_id = models.CharField(max_length=FieldLength.IDENTITY, unique=True)
    name = models.CharField(max_length=FieldLength.NAME)


@flowly_material('flowly.tests.content_root.sales')
class Service(MaterialMixin, models.Model):
    barcode_prefix = 'SRVC'
    barcode_field_name = 'unique_id'
    unique_id = models.CharField(max_length=FieldLength.IDENTITY, unique=True)
    name = models.CharField(max_length=FieldLength.NAME)


class ServiceOrderLineItem(models.Model):
    order = models.ForeignKey('ServiceOrder', on_delete=models.PROTECT)
    service = models.ForeignKey(Service, on_delete=models.PROTECT)
    quantity = models.IntegerField()


@flowly_material('flowly.tests.content_root.sales')
class ServiceOrder(MaterialMixin, models.Model):
    barcode_prefix = 'SO'
    barcode_field_name = 'unique_id'
    unique_id = models.CharField(max_length=FieldLength.IDENTITY, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    status = models.CharField(max_length=FieldLength.NAME, default='pending')
    line_items = models.ManyToManyField(Service, through=ServiceOrderLineItem)
    estimated_completion_date = models.DateField(null=True)

    def approve(self):
        self.status = 'approved'
        self.estimated_completion_date = datetime.date.today() + datetime.timedelta(weeks=3)
        self.save()


    def save(self, *args, **kwargs):
        super(MaterialMixin, self).save(*args, **kwargs)
        if not self.unique_id:
            self.unique_id = f'SO-{str(self.pk).zfill(6)}'
            self.save()