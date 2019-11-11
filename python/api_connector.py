import requests

from measurement import Measurement
from settings import API_ENDPOINT, DEVICE_ID, HEADER_API_USER_AGENT


def send_measurement(measurement: Measurement):
    json = measurement.as_dict()
    json['id'] = DEVICE_ID
    try:
        response = requests.post(url=API_ENDPOINT, json=json, headers={"user-agent": HEADER_API_USER_AGENT})
        return response.status_code in [200, 201]
    except Exception as e:
        # Failed to connect...
        return False
