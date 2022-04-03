from ...tags.objects import MaterialTag, DataTag, AssetTag
from . import run_tag_tests


def test_material_tag():
    run_tag_tests(
        tag_klass=MaterialTag,
        document='!Material identifier',
        expected_tag_name='!Material',
        expected_klass_name='Material',
        expected_value='identifier'
    )


def test_asset_tag():
    run_tag_tests(
        tag_klass=AssetTag,
        document='!Asset identifier',
        expected_tag_name='!Asset',
        expected_klass_name='Asset',
        expected_value='identifier'
    )


def test_data_tag():
    run_tag_tests(
        tag_klass=DataTag,
        document='!Data identifier',
        expected_tag_name='!Data',
        expected_klass_name='Data',
        expected_value='identifier'
    )
