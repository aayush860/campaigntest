# utils.py
import requests
from api_config import BASE_URL, HEADERS


def get(endpoint):
    response = requests.get(f"{BASE_URL}{endpoint}", headers=HEADERS)
    return response


def post(endpoint, data):
    response = requests.post(f"{BASE_URL}{endpoint}", json=data, headers=HEADERS)
    return response


def delete(endpoint):
    response = requests.delete(f"{BASE_URL}{endpoint}", headers=HEADERS)
    return response


def put(endpoint, data):
    response = requests.put(f"{BASE_URL}{endpoint}", json=data, headers=HEADERS)
    return response


def patch(endpoint, data):
    response = requests.patch(f"{BASE_URL}{endpoint}", json=data, headers=HEADERS)
    return response
