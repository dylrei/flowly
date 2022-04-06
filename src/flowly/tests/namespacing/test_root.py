from .. import content_root
from ...constants.runtime import IdentityConfigsKey
from ...namespacing.root import ContentRoot
from ...runtime import IdentityConfigs

def test_content_root():
    # We can't observe use of ContentRoot before it loads, but we can observe
    # the side-effects it had when it loaded
    expected_module_path = 'flowly.tests.content_root'
    assert IdentityConfigs.get(IdentityConfigsKey.CONTENT_ROOT) == expected_module_path
    assert IdentityConfigs.get(IdentityConfigsKey.PATH_TO_CONTENT_ROOT).split('/')[-1] == 'content_root'

    # loading a second ContentRoot is not allowed
    try:
        ContentRoot(module_namespace='some.namespace', file_path='path/to/some/namespace')
        success = True
    except RuntimeError as err:
        success = False
        assert 'Attempt to set IdentityConfigs key content_root' in str(err)
    assert success is False

    # but if you end up invoking the same ContentRoot many times, no big deal
    assert IdentityConfigs.get(IdentityConfigsKey.CONTENT_ROOT) == expected_module_path
    ContentRoot(expected_module_path, IdentityConfigs.get(IdentityConfigsKey.PATH_TO_CONTENT_ROOT))
    assert IdentityConfigs.get(IdentityConfigsKey.CONTENT_ROOT) == expected_module_path
