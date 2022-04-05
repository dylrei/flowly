from ...runtime.truth import SourceOfTruth


def test_source_of_truth():
    my_attr = 'my_attr'

    class MySOT(SourceOfTruth):
        managed_names = {
            my_attr: None
        }
    initial_value = 'Tuvok'
    unwelcome_value = 'Tuvix'

    # initial state
    assert MySOT.get(my_attr) is None

    # attr value changes when set once
    MySOT.set(my_attr, initial_value)
    assert MySOT.get(my_attr) == initial_value

    # subsequent attempts set attr to same value are ignored
    MySOT.set(my_attr, initial_value)
    assert MySOT.get(my_attr) == initial_value

    # attempting to set a SOT attr to a new value is evidence of a problem and raises an exception
    try:
        MySOT.set(my_attr, unwelcome_value)
        success = True
    except RuntimeError as err:
        success = False
        assert 'Attempt to set MySOT key my_attr to more than one value' in str(err)
    assert success is False

    # attempting to instantiate an SOT is bad manners
    try:
        sot = MySOT()
        success = True
    except RuntimeError as err:
        success = False
        assert 'Attempt to initialize SourceOfTruth subclass' in str(err)
    assert success is False
