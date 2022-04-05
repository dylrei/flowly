from ...constants.runtime import IdentityConfigsKey
from ...namespacing.root import ContentRoot
from ...runtime import IdentityConfigs
from ...tests import import_target


def test_content_root():
    # We can't observe use of ContentRoot before it loads, but we can observe
    # the side-effects it had when it loaded
    module_path_of_tests_dir = import_target.__module__
    assert IdentityConfigs.get(IdentityConfigsKey.CONTENT_ROOT) == module_path_of_tests_dir

    # loading a second ContentRoot is not allowed
    try:
        ContentRoot(__name__)
        success = True
    except RuntimeError as err:
        success = False
        assert 'Attempt to set IdentityConfigs key content_root' in str(err)
    assert success is False

    # but if you end up invoking the same ContentRoot many times, no big deal
    assert IdentityConfigs.get(IdentityConfigsKey.CONTENT_ROOT) == module_path_of_tests_dir
    ContentRoot(module_path_of_tests_dir)
    assert IdentityConfigs.get(IdentityConfigsKey.CONTENT_ROOT) == module_path_of_tests_dir
