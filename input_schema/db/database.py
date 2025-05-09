from input_schema.base import InputSchemaBase
from typing import TypeVar, Generic
import json


T = TypeVar('T', bound=InputSchemaBase)


class Database(Generic[T]):

    def __init__(self, file, element_class: type[T], unique_key: str = 'ID', ):
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

    def get_ids(self) -> list[int]:
        return list(self.data.keys())

    def __getitem__(self, item: int) -> T:
        return self.data[item]