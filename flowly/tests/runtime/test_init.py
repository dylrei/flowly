from ...constants.runtime import IdentityConfigsKey
from ...runtime import IdentityConfigs, SourceOfTruth


def test_identity_configs():
    # True story: we can't actually test the *unconfigured* IdentityConfigsKey
    # because the one we are using for testing is modified before any tests run
    # So there isn't really a chance to observe the "first set"
    # moment because that happens before any testing, when tests/ first loads and sets content_root :)
    # Anyway, we demonstrated first-set behavior in the base class and here we will
    # simply prove that what we are testing subclasses that
    assert issubclass(IdentityConfigs, SourceOfTruth) is True

    # show that we can set the same value again, no problem
    content_root = IdentityConfigs.get(IdentityConfigsKey.CONTENT_ROOT)
    IdentityConfigs.set(IdentityConfigsKey.CONTENT_ROOT, content_root)
    assert IdentityConfigs.get(IdentityConfigsKey.CONTENT_ROOT) == content_root

    # set value to something else, we have a problem
    try:
        IdentityConfigs.set(IdentityConfigsKey.CONTENT_ROOT, 'something new')
        success = True
    except RuntimeError as err:
        success = False
        assert 'Attempt to set IdentityConfigs key content_root to more than one value' in str(err)
    assert success is False
