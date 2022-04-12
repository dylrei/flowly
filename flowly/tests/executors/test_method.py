import pytest

from ..content_root.sales.create_sale import create_sale_1_0
from ..content_root.specifications.testing import calculate_total
from ...stores.method import MethodStore

pytestmark = pytest.mark.django_db


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

    # first step
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

    first_run_state_id = result['state']
    # second step
    test_data = {
        'cash_tendered': 5.00,
    }
    result = method.run(test_data, first_run_state_id)
    assert result['method'] == method_identity
    assert result['node'] == 'create_sale'
    assert 'timestamp' in result
    assert 'state' in result
    assert result['data']['result'] == {
        'customer': 'finance/lists::CUST-123',
        'order_number': 'ORD-1234',
        'total_cost': 3.14
    }
    assert result['data']['completed'] is True
