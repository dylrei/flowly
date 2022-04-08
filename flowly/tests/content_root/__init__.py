from ...namespacing.root import ContentRoot

# we may only load executors/documents in or below this directory
_module_namespace = __name__
_file_path = __file__
content_root = ContentRoot(module_namespace=_module_namespace, file_path=_file_path)
