from excel_files import ExcelOutputFile
from abc import ABC, abstractmethod
from pathlib import Path

import json
import logging

class FileParserBase(ABC):

    EXCEL_OUTPUT_PATH = Path('../ExcelOutput')
    TEXT_MAPS_PATH = Path('../TextMap')
    text_map: dict[str, str] = {}

    def __init__(self, lang: str = 'EN'):
        self.lang = lang
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    @abstractmethod
    def open(self):
        ...

    def _unhash(self, hash_value: int) -> str:
        return self.text_map.get(str(hash_value), '<Unknown Hash>')

    def _initialize_paths(self):
        with open(self.EXCEL_OUTPUT_PATH / ExcelOutputFile.AVATAR_PATHS.value, 'r', encoding='utf-8') as file:
            path_list = json.load(file)
            self.class_to_path = {}
            for path in path_list:
                if 'ID' not in path:
                    continue
                self.class_to_path[path['ID']] = self._unhash(path['BaseTypeText']['Hash'])

    def _get_path(self, path_id: str) -> str:
        return self.class_to_path.get(path_id, 'General')

    def _initialize_text_map(self):
        with open(self.TEXT_MAPS_PATH / f'TextMap{self.lang}.json', 'r', encoding='utf-8') as file:
            self.text_map = json.load(file)
            self.logger.debug(f"Loaded text map for language {self.lang}: {len(self.text_map)} entries")