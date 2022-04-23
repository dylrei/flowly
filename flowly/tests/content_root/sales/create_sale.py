from flowly.decorators import identified_executor


@identified_executor('sales::create_sale==production')
@identified_executor('sales::create_sale==1.0')
def create_sale_1_0(funds_applied, customer, items, total_cost):
    return 'ORD-1234'
