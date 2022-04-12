from ..content_root.specifications.testing import calculate_total
from ...stores.method import MethodStore


def test_method_executor_one_step():
    method_identity = 'sales/cash::make_cash_sale==0.9'
    method = MethodStore.load(method_identity)
    test_data = {
        'customer': 'finance/lists::CUST-123',
        'items': ['sales/items::ITEM-777', 'sales/items::ITEM-888', 'sales/items::ITEM-999']
    }
    result = method.run(test_data)
    assert result['method'] == method_identity
    assert result['node'] == 'calculate_total'
    assert 'timestamp' in result
    assert 'state' in result
    assert result['data']['result'] == {'customer': 'finance/lists::CUST-123', 'order_total': 3.14, 'total_cost': 3.14}
    assert result['data']['completed'] is True


def test_method_executor_two_step():
    method_identity = 'sales/cash::make_cash_sale==1.0'
    method = MethodStore.load(method_identity)
    test_data = {
        'customer': 'finance/lists::CUST-123',
        'items': ['sales/items::ITEM-777', 'sales/items::ITEM-888', 'sales/items::ITEM-999']
    }
    result = method.run(test_data)
    assert result['method'] == method_identity
    assert result['node'] == 'calculate_total'
    assert 'timestamp' in result
    assert 'state' in result
    assert result['data']['result'] == {'order_total': 3.14}
    assert result['data']['completed'] is False
