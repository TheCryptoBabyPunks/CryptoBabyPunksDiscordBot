import requests
from config import Config

class PunksFamilyAPI:

    def __init__(self):
        self.path = "https://punks.family/api/punks"

    def get(self, code):
        url = self.path + '/' +code
        headers = { 'Authorization': 'Bearer '+Config.PF_TOKEN }
        response = requests.request("GET", url, headers=headers)
        return response.json()
