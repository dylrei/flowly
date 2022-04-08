from ..constants.runtime import IdentityConfigsKey
from ..runtime import IdentityConfigs


class ContentRoot(object):
    def __init__(self, module_namespace, file_path):
        # register highest-level module that namespace executors must be a child of
        IdentityConfigs.set(IdentityConfigsKey.CONTENT_ROOT, module_namespace)

        # register the absolute file path to content root directory
        if file_path.endswith('.py'):
            file_path = '/'.join(file_path.split('/')[:-1])
        IdentityConfigs.set(IdentityConfigsKey.PATH_TO_CONTENT_ROOT, file_path)
