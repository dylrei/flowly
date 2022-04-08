from .core.math.subtract import subtract_1_0
from .executors.test_identified.test_fx import one_implementation, another_implementation, yet_another_implementation, \
    do_not_use_this_version_unless_you_are_me
from ...namespacing.root import ContentRoot

# we may only load executors/documents in or below this directory
_module_namespace = __name__
_file_path = __file__
content_root = ContentRoot(module_namespace=_module_namespace, file_path=_file_path)

_imported_executors = [
    # core/math/subtract
    subtract_1_0,
    # executors/test_identified
    one_implementation, another_implementation, yet_another_implementation, do_not_use_this_version_unless_you_are_me
]