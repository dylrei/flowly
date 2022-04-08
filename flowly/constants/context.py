from constant_namespace import ConstantNamespace


class DocumentLoaderContext(ConstantNamespace):
    # there is no inherent document "type" only the context in which it is loaded
    IDENTITY = 'identity'
    SPECIFICATION = 'specification'
    METHOD = 'method'
