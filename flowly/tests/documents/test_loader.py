from ...constants.tags import TagName
from ...documents.loader import load_yaml_document
from ...documents.tags import ActionTag


def test_load_yaml():
    document = '''
- !META
  domain: sales/cash
  name: make_cash_sale
  version: 1.0
  status: testing

- !BODY
  - !Step
    name: calculate_total
    description: a step where we calculate what the order total would be
    input: specifications/testing::simple_yaml_spec==1.0
    body:
      - !Action
        id: specifications/testing::calculate_total==1.0
        customer: !Material customer
        items: !Materials selected_items
        store: !State order_total
    return:
      order_total: !State order_total

  - !Step
    name: create_sale
    input: specifications/testing::cash_tendered==1.0
    body:
      - !Action
        id: specifications/testing::subtract==1.0
        left: !State order_total
        right: !State cash_tendered
        store: !State change_due
      - !Action
        id: specifications/testing::create_sale==1.0
        # cash_tendered came from input for this step
        funds_applied: !State cash_tendered
        # these values are persisted from the previous step / request
        customer: !Material customer
        items: !Materials selected_items
        total_cost: !State order_total
        store: !State order_number
    return:
      foo: bar
    '''

    result = load_yaml_document(document)
    meta_node = result[TagName.META]
    assert meta_node.tag == TagName.META
    assert meta_node.value == {'domain': 'sales/cash', 'name': 'make_cash_sale', 'version': '1.0', 'status': 'testing'}

    body_node = result[TagName.BODY]
    assert body_node.tag == TagName.BODY
    first_step_node = body_node.value[0]
    assert first_step_node.tag == TagName.Step
    assert first_step_node.value['name'] == 'calculate_total'
    action_node = first_step_node.value['body'][0]
    assert action_node.tag == TagName.Action
    assert isinstance(action_node, ActionTag)
    assert action_node.value['id'] == 'specifications/testing::calculate_total==1.0'

    second_step_node = body_node.value[1]
    assert second_step_node.tag == TagName.Step
    assert second_step_node.value['name'] == 'create_sale'
    first_action_node = second_step_node.value['body'][0]
    assert first_action_node.tag == TagName.Action
    assert isinstance(first_action_node, ActionTag)
    assert first_action_node.value['id'] == 'specifications/testing::subtract==1.0'
    second_action_node = second_step_node.value['body'][1]
    assert second_action_node.tag == TagName.Action
    assert isinstance(second_action_node, ActionTag)
    assert second_action_node.value['id'] == 'specifications/testing::create_sale==1.0'
