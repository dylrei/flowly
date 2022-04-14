import uuid

import pytest

from flowly.executors.method import Data, State
from flowly.models import Run
from flowly.utils.method import load_data_and_state

pytestmark = pytest.mark.django_db


def test_load_data_and_state():
    test_data = {
        'name': 'Roo',
        'favorite_word': 'qwrad'
    }
    to_persist = {
        'name': 'Smoo',
        'favorite_word': 'florb'
    }
    method_id = 'fake/namespace::not_used==1.0'
    run = Run.objects.create(identity=str(uuid.uuid4()), method=method_id)
    data, state, state_loaded = load_data_and_state(run_obj=run,
                                                    data_provided=test_data,
                                                    state_identity=None)
    assert isinstance(data, Data) is True
    assert data.method_id == method_id
    assert data.value == test_data

    assert state_loaded is False
    assert isinstance(state, State) is True
    assert state.method_id == method_id
    assert state.value == dict()
    assert state.run == run

    # add data to state and persist it
    state.update(to_persist)
    state.persist()

    # now load new state object with that data by using the previous state's identity
    new_run = Run.objects.create(identity=str(uuid.uuid4()), method=method_id)
    new_data, new_state, new_state_loaded = load_data_and_state(run_obj=new_run,
                                                                data_provided=test_data,
                                                                state_identity=state.identity)
    # same as before
    assert isinstance(new_data, Data) is True
    assert new_data.method_id == method_id
    assert new_data.value == test_data

    # state successfully loaded from identity
    assert new_state_loaded is True
    assert isinstance(new_state, State) is True
    assert new_state.method_id == method_id
    assert new_state.value == to_persist
    assert new_state.run == new_run



