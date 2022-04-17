from flowly.executors.identified import identified_executor


@identified_executor('math::subtract==production')
@identified_executor('math::subtract==1.0')
def subtract_1_0(left, right):
    return left - right
