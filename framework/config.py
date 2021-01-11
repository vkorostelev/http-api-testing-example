from os import getenv

SERVICE_URL = getenv('SERVICE_URL', 'http://0.0.0.0:4000')
USE_MOCK = (getenv('USE_MOCK', True)) in (True, 'True', 'true', 1)
