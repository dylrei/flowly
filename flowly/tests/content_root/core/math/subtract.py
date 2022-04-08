from flowly.executors.identified import identified_executor


@identified_executor('core/math::subtract==production')
@identified_executor('core/math::subtract==1.0')
def subtract_1_0(left, right):
    return left - right
