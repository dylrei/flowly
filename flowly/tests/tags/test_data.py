from ..tags import run_tag_tests
from ...constants.tags import TagName


def test_state_tag():
    run_tag_tests(
        document='!State field_key',
        expected_tag_name=TagName.State,
        expected_value='field_key'
    )


def test_input_tag():
    run_tag_tests(
        document='!Input field_key',
        expected_tag_name='!Input',
        expected_value='field_key'
    )
