from input_schema.base import InputSchemaBase
import json


class Database:

    def __init__(self, file, unique_key: str = 'ID', element_class: type = InputSchemaBase):
        self.unique_key = unique_key
        self.element_class = element_class
        self.file = file
        self.data = {}

    def load(self, text_map: dict[str, str]):
        for element in json.load(self.file):
            element_id = element[self.unique_key]
            if element_id not in self.data:
                self.data[element_id] = self.element_class(text_map)
            self.data[element_id].update(element)
