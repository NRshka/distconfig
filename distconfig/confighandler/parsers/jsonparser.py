import json

from .parser import AbstractConfigParser


class JSONParser(AbstractConfigParser):
    @staticmethod
    def parse(path: str) -> dict:
        with open(path, 'r') as file:
            return json.load(file)
