from flowly.executors.identified import identified_executor


@identified_executor('core/math::add==production')
@identified_executor('core/math::add==1.0')
def add_1_0(numbers):
    running_total = None
    for number in numbers:
        if running_total is None:
            running_total = number
        else:
            running_total += number
    return running_total
