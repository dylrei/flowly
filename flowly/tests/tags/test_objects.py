from . import run_tag_tests


def test_material_tag():
    run_tag_tests(
        document='!Material identifier',
        expected_tag_name='!Material',
        expected_value='identifier'
    )


def test_asset_tag():
    run_tag_tests(
        document='!Asset identifier',
        expected_tag_name='!Asset',
        expected_value='identifier'
    )

