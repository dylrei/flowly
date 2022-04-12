from .....executors.identified import identified_executor


@identified_executor('specifications/testing::calculate_total==1.0')
def calculate_total(customer, items):
    return 3.14
