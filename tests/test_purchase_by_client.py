from datetime import datetime

import pytest

from hamcrest import assert_that, is_, has_length, has_item, has_entries, greater_than


def test_get_purchase_after_creating_order(payload_generator, service_api):
    client_payload = payload_generator.client_request_payload()
    client_id = service_api.create_client(client_payload).json()['client_id']

    order_payload = payload_generator.order_request_payload(client_id, client_payload['phone'], 1)
    order_data = service_api.create_order(order_payload).json()

    purchase_payload = {
        "client_id": client_id,
        "item_ids": [
            str(order_payload['items'][0]['item_id'])
        ]
    }

    expected_purchase_item = {
        'item_id': purchase_payload['item_ids'][0],
        'last_order_number': order_data['order_number'],
        'purchase_count': order_payload['items'][0]['quantity'],
        'purchased': True
    }

    response = service_api.get_item_purchase_by_client(purchase_payload, mock_data={'items': [expected_purchase_item]})

    assert_that(response.status_code, is_(200))
    assert_that(response.json()['items'], has_length(1))
    assert_that(response.json()['items'], has_item(has_entries(expected_purchase_item)))


def test_get_purchase_after_order_multiple_items_in_one_order(payload_generator, service_api):
    client_payload = payload_generator.client_request_payload()
    client_id = service_api.create_client(client_payload).json()['client_id']

    order_payload = payload_generator.order_request_payload(client_id, client_payload['phone'], 2)
    order_data = service_api.create_order(order_payload).json()

    purchase_payload = {
        "client_id": client_id,
        "item_ids": [
            str(order_payload['items'][0]['item_id']),
            str(order_payload['items'][1]['item_id'])
        ]
    }

    expected_purchase_items = [
        {
            'item_id': purchase_payload['item_ids'][0],
            'last_order_number': order_data['order_number'],
            'purchase_count': order_payload['items'][0]['quantity'],
            'purchased': True
        },
        {
            'item_id': purchase_payload['item_ids'][1],
            'last_order_number': order_data['order_number'],
            'purchase_count': order_payload['items'][1]['quantity'],
            'purchased': True
        }
    ]

    response = service_api.get_item_purchase_by_client(purchase_payload, mock_data={'items': expected_purchase_items})

    assert_that(response.status_code, is_(200))
    assert_that(response.json()['items'], has_length(2))
    assert_that(response.json()['items'], has_item(has_entries(expected_purchase_items[0])))
    assert_that(response.json()['items'], has_item(has_entries(expected_purchase_items[1])))


def test_get_purchase_after_order_same_item_multiple_times(payload_generator, service_api):
    client_payload = payload_generator.client_request_payload()
    client_id = service_api.create_client(client_payload).json()['client_id']

    order_payload = payload_generator.order_request_payload(client_id, client_payload['phone'], 1)
    service_api.create_order(order_payload).json()
    second_order_data = service_api.create_order(order_payload).json()

    purchase_payload = {
        "client_id": client_id,
        "item_ids": [
            str(order_payload['items'][0]['item_id'])
        ]
    }

    expected_purchase_item = {
        'item_id': purchase_payload['item_ids'][0],
        'last_order_number': second_order_data['order_number'],
        'purchase_count': order_payload['items'][0]['quantity'] * 2,
        'purchased': True
    }

    response = service_api.get_item_purchase_by_client(purchase_payload, mock_data={'items': [expected_purchase_item]})

    assert_that(response.status_code, is_(200))
    assert_that(response.json()['items'], has_length(1))
    assert_that(response.json()['items'], has_item(has_entries(expected_purchase_item)))


def test_get_purchase_after_order_multiple_different_items(payload_generator, service_api):
    client_payload = payload_generator.client_request_payload()
    client_id = service_api.create_client(client_payload).json()['client_id']

    first_order_payload = payload_generator.order_request_payload(client_id, client_payload['phone'], 1)
    first_order_data = service_api.create_order(first_order_payload).json()

    second_order_payload = payload_generator.order_request_payload(client_id, client_payload['phone'], 1)
    second_order_data = service_api.create_order(second_order_payload).json()

    purchase_payload = {
        "client_id": client_id,
        "item_ids": [
            str(first_order_payload['items'][0]['item_id']),
            str(second_order_payload['items'][0]['item_id'])
        ]
    }

    expected_purchase_items = [
        {
            'item_id': purchase_payload['item_ids'][0],
            'last_order_number': first_order_data['order_number'],
            'purchase_count': first_order_payload['items'][0]['quantity'],
            'purchased': True
        },
        {
            'item_id': purchase_payload['item_ids'][1],
            'last_order_number': second_order_data['order_number'],
            'purchase_count': second_order_payload['items'][0]['quantity'],
            'purchased': True
        }
    ]

    response = service_api.get_item_purchase_by_client(purchase_payload, mock_data={'items': expected_purchase_items})

    assert_that(response.status_code, is_(200))
    assert_that(response.json()['items'], has_length(2))
    assert_that(response.json()['items'], has_item(has_entries(expected_purchase_items[0])))
    assert_that(response.json()['items'], has_item(has_entries(expected_purchase_items[1])))


def test_purchase_by_client_multiple_calls_return_same_result(payload_generator, service_api):
    client_payload = payload_generator.client_request_payload()
    client_id = service_api.create_client(client_payload).json()['client_id']

    order_payload = payload_generator.order_request_payload(client_id, client_payload['phone'], 1)
    order_data = service_api.create_order(order_payload).json()

    purchase_payload = {
        "client_id": client_id,
        "item_ids": [
            str(order_payload['items'][0]['item_id'])
        ]
    }

    mock_data = {'items': [{
        'item_id': purchase_payload['item_ids'][0],
        'last_order_number': order_data['order_number'],
        'purchase_count': order_payload['items'][0]['quantity'],
        'purchased': True
    }]}

    first_response = service_api.get_item_purchase_by_client(purchase_payload, mock_data=mock_data)
    second_response = service_api.get_item_purchase_by_client(purchase_payload, mock_data=mock_data)
    assert_that(first_response.status_code, is_(second_response.status_code))
    assert_that(first_response.json(), is_(second_response.json()))


def test_get_purchase_by_client_last_purchase_date(payload_generator, service_api):
    client_payload = payload_generator.client_request_payload()
    client_id = service_api.create_client(client_payload).json()['client_id']

    datetime_before_order = datetime.now()
    order_payload = payload_generator.order_request_payload(client_id, client_payload['phone'], 1)
    service_api.create_order(order_payload).json()

    purchase_payload = {
        "client_id": client_id,
        "item_ids": [
            str(order_payload['items'][0]['item_id'])
        ]
    }

    mock_data = {
        'items': [{
            'last_purchase_date': datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        }]
    }
    response = service_api.get_item_purchase_by_client(purchase_payload, mock_data=mock_data)

    last_purchase_date = datetime.strptime(response.json()['items'][0]['last_purchase_date'], '%Y-%m-%dT%H:%M:%S.%fZ')
    assert_that(last_purchase_date, is_(greater_than(datetime_before_order)))


@pytest.mark.parametrize('purchase_payload', [
    pytest.param({
        "client_id": '1',
    }, id="without item_ids"),
    pytest.param({
        "item_ids": ['1']
    }, id="without client_id"),
    pytest.param({
        "client_id": '1',
        "item_ids": []
    }, id="with empty item_ids list"),
    pytest.param({}, id="without any field")
])
def test_purchase_by_client_with_no_required_fields(purchase_payload, service_api):
    response = service_api.get_item_purchase_by_client(purchase_payload, mock_status=400)
    assert_that(response.status_code, is_(400))


@pytest.mark.parametrize('purchase_payload', [
    {
        "client_id": 'non_existing_id',
        "item_ids": ['1']
    },
    {
        "client_id": '1',
        "item_ids": ['non_existing_id']
    },
    {
        "client_id": '1',
        "item_ids": ['1', 'non_existing_id']
    }
])
def test_purchase_by_client_with_not_existing_ids(purchase_payload, service_api):
    response = service_api.get_item_purchase_by_client(purchase_payload, mock_status=404)
    assert_that(response.status_code, is_(404))
