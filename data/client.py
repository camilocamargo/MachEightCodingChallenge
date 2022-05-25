import requests


class Client:
    def __init__(self, url):
        self.url = url

    def get(self):
        result = requests.get(self.url)
        return result
