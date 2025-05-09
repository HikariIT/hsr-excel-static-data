from abc import ABC, abstractmethod

class InputSchemaBase(ABC):

    def __init__(self, text_map: dict[str, str]):
        self.text_map = text_map

    def _unhash(self, hash_value: int) -> str:
        return self.text_map.get(str(hash_value), '<Unknown Hash>')

    @abstractmethod
    def update(self, schema: dict) -> None:
        ...