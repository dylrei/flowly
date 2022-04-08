from ..stores.identified_executor import IdentifiedExecutorStore


def identified_executor(identity):
    def registration_wrapper(fx):
        IdentifiedExecutorStore.register(identity, fx)
        return fx
    return registration_wrapper
