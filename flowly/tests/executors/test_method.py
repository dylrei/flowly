# from datetime import datetime
import datetime

import pytest

from ..content_root.sales import create_sale
from ..content_root.specifications.testing import calculate_total
from ...constants.payload import PayloadKey
from ...stores.method import MethodStore
from ...utils.payload import is_uuid

pytestmark = pytest.mark.django_db


def test_method_executor_one_step():
    method_identity = 'sales/cash::make_cash_sale==0.9'
    method = MethodStore.load(method_identity)
    test_data = {
        'customer': 'finance/lists::CUST-123',
        'items': ['sales/items::ITEM-777', 'sales/items::ITEM-888', 'sales/items::ITEM-999']
    }
    result = method.run(test_data)
    assert result[PayloadKey.REQUEST][PayloadKey.METHOD] == method_identity
    assert result[PayloadKey.REQUEST][PayloadKey.NODE] == 'calculate_total'
    assert is_uuid(result[PayloadKey.REQUEST][PayloadKey.STATE])
    assert result[PayloadKey.REQUEST][PayloadKey.COMPLETED] is True
    assert result[PayloadKey.DATA] == {'customer': 'finance/lists::CUST-123', 'order_total': 3.14, 'total_cost': 3.14}
    assert result[PayloadKey.NEXT] == {}
    assert isinstance(result[PayloadKey.TIMESTAMP], datetime.datetime)


def test_method_executor_two_step():
    method_identity = 'sales/cash::make_cash_sale==1.0'
    method = MethodStore.load(method_identity)

    # first step
    test_data = {
        'customer': 'finance/lists::CUST-123',
        'items': ['sales/items::ITEM-777', 'sales/items::ITEM-888', 'sales/items::ITEM-999']
    }
    result = method.run(test_data)
    assert result[PayloadKey.REQUEST][PayloadKey.METHOD] == method_identity
    assert result[PayloadKey.REQUEST][PayloadKey.NODE] == 'calculate_total'
    assert is_uuid(result[PayloadKey.REQUEST][PayloadKey.STATE])
    assert result[PayloadKey.REQUEST][PayloadKey.COMPLETED] is False
    assert result[PayloadKey.DATA] == {'order_total': 3.14}
    assert result[PayloadKey.NEXT] == {k: v for k, v in result[PayloadKey.REQUEST].items() if k != PayloadKey.COMPLETED}
    first_run_state_id = result[PayloadKey.REQUEST][PayloadKey.STATE]

    # second step
    test_data = {
        'cash_tendered': 5.00,
    }
    result = method.run(test_data, first_run_state_id)
    assert result[PayloadKey.REQUEST][PayloadKey.METHOD] == method_identity
    assert result[PayloadKey.REQUEST][PayloadKey.NODE] == 'create_sale'
    assert is_uuid(result[PayloadKey.REQUEST][PayloadKey.STATE])
    assert result[PayloadKey.REQUEST][PayloadKey.COMPLETED] is True
    assert result[PayloadKey.DATA] == {'customer': 'finance/lists::CUST-123',
                                       'order_number': 'ORD-1234',
                                       'total_cost': 3.14}
    assert result[PayloadKey.NEXT] == {}
    assert isinstance(result[PayloadKey.TIMESTAMP], datetime.datetime)
