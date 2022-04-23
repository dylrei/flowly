from flowly.executors.identified import identified_executor


@identified_executor('core/math::subtract==production')
@identified_executor('core/math::subtract==1.0')
def multiply_1_0(numbers):
    running_total = None
    for number in numbers:
        if running_total is None:
            running_total = number
        else:
            running_total -= number
    return running_total
