# from ...tags.loader import load_yaml
#
# def _test_keyword_tag(name, value):
#     obj = load_yaml(f'!{name} {value}')
#     assert obj.__class__.__name__ == name
#     assert obj.tag.tag_name == f'!{name}'
#     assert obj.value == value
#
#
# def _test_fail_case(name, value):
#     failure_observed = False
#     try:
#         obj = load_yaml(f'!{name} {value}')
#     except:
#         failure_observed = True
#     if not failure_observed:
#         raise RuntimeError(f'Expected failure: "!{name} {value}"')
#
#
# def test_keywords():
#     happy_cases = [
#         # (tag/class name, example value)
#         ('DataType', 'string'),
#         ('Domain', 'foo/bar'),
#         ('Method', 'do_something'),
#         ('Version', '1.0'),
#         ('Status', 'production'),
#         ('Doctype', 'specification')
#     ]
#
#     fail_cases = [
#         ('NoneSuch', 'ignore me'),
#         ('DataType', 'something invalid'),
#     ]
#
#     for case in happy_cases:
#         _test_keyword_tag(*case)
#
#     for case in fail_cases:
#         _test_fail_case(*case)
#
# def test_empty_keyword():
#     obj = load_yaml('!Method')
#     import ipdb; ipdb.set_trace()
#     pass