import requests
import requests_mock

from .payload_generator import PayloadGenerator


class ServiceAPI:
    def __init__(self, api_url: str, use_mock: bool):
        self._api_url = api_url + '/service/v1'
        self.use_mock = use_mock

    def create_client(self, payload: dict) -> requests.Response:
        url = self._api_url + '/client/create'

        with requests_mock.Mocker(real_http=True) as mock:
            if self.use_mock:
                mock.post(url, json=PayloadGenerator.client_response_payload())

            return requests.post(self._api_url + '/client/create', json=payload)

    def create_order(self, payload: dict) -> requests.Response:
        url = self._api_url + '/order/create'

        with requests_mock.Mocker(real_http=True) as mock:
            if self.use_mock:
                mock.post(url, json=PayloadGenerator.order_response_payload())

            return requests.post(url, json=payload)

    def get_item_purchase_by_client(self, payload: dict, *,
                                    mock_data: dict = None, mock_status: int = None) -> requests.Response:
        purchase_by_client_url = self._api_url + '/item/purchase/by-client'

        with requests_mock.Mocker(real_http=True) as mock:
            if self.use_mock and mock_data:
                mock.get(purchase_by_client_url, json=mock_data)
            if self.use_mock and mock_status:
                mock.get(purchase_by_client_url, status_code=mock_status)

            return requests.get(purchase_by_client_url, json=payload)
