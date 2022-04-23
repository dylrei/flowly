from collections import Counter

from flowly.decorators import identified_executor
from flowly.models import ServiceOrder, ServiceOrderLineItem


@identified_executor('service::create_service_order==production')
@identified_executor('service::create_service_order==1.0')
def create_service_order_1_0(customer, services):
    service_order = ServiceOrder.objects.create(customer=customer)
    ServiceOrderLineItem.objects.bulk_create(
        [
            ServiceOrderLineItem(
                order=service_order,
                service=service,
                quantity=qty
            )
            for service, qty in Counter(services).items()
        ]
    )
    return service_order
