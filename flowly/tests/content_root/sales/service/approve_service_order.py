from flowly.decorators import identified_executor


@identified_executor('service::approve_service_order==production')
@identified_executor('service::approve_service_order==1.0')
def approve_service_order_1_0(service_order, approved):
    if approved:
        service_order.approve()
        service_order.refresh_from_db()
    return service_order
