import requests

class XController:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get(self, endpoint: str, params=None):
        response = requests.get(f"{self.base_url}/{endpoint}", params=params)
        response.raise_for_status()
        return response.json()

    def post(self, endpoint: str, data=None):
        response = requests.post(f"{self.base_url}/{endpoint}", json=data)
        response.raise_for_status()
        return response.json()

    def put(self, endpoint: str, data=None):
        response = requests.put(f"{self.base_url}/{endpoint}", json=data)
        response.raise_for_status()
        return response.json()

    def delete(self, endpoint: str):
        response = requests.delete(f"{self.base_url}/{endpoint}")
        response.raise_for_status()
        return response.status_code