from faker import Faker

fake = Faker('ru_RU')


class PayloadGenerator:
    @staticmethod
    def client_request_payload():
        return {
            "name": fake.first_name_male(),
            "surname": fake.last_name_male(),
            "phone": fake.phone_number()
        }

    @staticmethod
    def client_response_payload():
        return {
            "client_id": fake.unique.random_int(),
        }

    @staticmethod
    def order_request_payload(client_id: str, client_phone: str = None, items_count: int = 1):
        return {
            "client_id": client_id,
            "address": "".join((fake.country(), fake.region(), fake.street_address())),
            "phone": client_phone if client_phone else fake.phone_number(),
            "items": [
                {
                    "item_id": fake.unique.random_int(),
                    "price": fake.unique.random_int() + 1 / fake.unique.random_int(),
                    "quantity": fake.unique.random_digit(),
                } for _ in range(items_count)
            ]
        }

    @staticmethod
    def order_response_payload():
        return {
            "order_id": fake.unique.random_int(),
            "order_number": fake.unique.random_int(),
        }
