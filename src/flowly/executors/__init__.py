class VersionedExecutor(object):
    def __init__(self, version_mapping):
        # version_mapping is locals() of the wrapped function
        self.version_mapping = version_mapping

    def __call__(self, *args, _version='default', **kwargs):
        return self.version_mapping[_version](*args, **kwargs)


def versioned_executor(func, *args, **kwargs):
    return VersionedExecutor(func())
