from flowly.stores.names import NameStore


def identified_executor(identity):
    def registration_wrapper(fx):
        namespace = _find_namespace(fx)
        namespace.register(identity, fx)
        return fx
    return registration_wrapper


def flowly_material(namespace_identity):
    def registration_wrapper(model):
        NameStore.register_model(namespace_identity, model)
        return model
    return registration_wrapper


def _find_namespace(fx):
    fx_module_path = fx.__module__
    module_path_elems = fx_module_path.split('.')
    for offset in range(1, len(module_path_elems)):
        ns_identity = '.'.join(module_path_elems[:-1 * offset])
        if NameStore.exists(ns_identity):
            return NameStore.get_namespace(ns_identity)
    raise RuntimeError(f'No namespace found for {fx_module_path}')
