from ..constants.runtime import IdentityConfigsKey
from ..runtime import IdentityConfigs


class ContentRoot(object):
    def __init__(self, module_namespace):
        IdentityConfigs.set(IdentityConfigsKey.CONTENT_ROOT, module_namespace)
