import pathlib
import json
import os

from generated.character.enums.damage_type import DamageType
from generated.character.enums.rarity import Rarity
from generated.character.enums.path import Path
from schema.output import CharacterOutput


class JsonClassSerializer:

    def __init__(self, json_data: CharacterOutput):
        self.json_data = json_data

    def _get_preamble(self) -> str:
        imports = {
            '_character_base': ['CharacterBase'],
            'enums.rarity': ['Rarity'],
            'enums.path': ['Path'],
            'enums.damage_type': ['DamageType'],
        }

        preamble = "# This file is auto-generated. Do not edit.\n\n"
        for module, class_names in imports.items():
            preamble += f"from {module} import {', '.join(class_names)}\n"
        preamble += "\n\n"
        return preamble


    def _get_class_definition(self) -> str:
        class_definition = f"class {self._get_character_name()}(CharacterBase):\n"
        return class_definition

    def _get_basic_class_attributes(self) -> str:
        class_text = ''
        attribute_classes = {
            'id': 'str',
            'name': 'str',
            'rarity': 'Rarity',
            'path': 'Path',
            'damage_type': 'DamageType',
        }

        attribute_values = {
            'id': self.json_data.id,
            'name': self.json_data.name,
            'rarity': Rarity.FIVE_STAR if self.json_data.rarity == 5 else Rarity.FOUR_STAR,
            'path': Path._get_from_string(self.json_data.path),
            'damage_type': DamageType._get_from_string(self.json_data.damage_type),
        }

        for attr_name in attribute_classes:
            attr_type = attribute_classes[attr_name]
            attr_value = attribute_values[attr_name]

            if isinstance(attr_value, str):
                attr_value = f"'{attr_value}'"
            elif isinstance(attr_value, int):
                attr_value = str(attr_value)
            elif isinstance(attr_value, float):
                attr_value = str(attr_value)
            elif isinstance(attr_value, bool):
                attr_value = str(attr_value).lower()

            class_text += self._indent(f"{attr_name}: {attr_type} = {attr_value}\n", 1)

        if self.json_data.max_energy is not None:
            class_text += self._indent(f"max_energy: int = {self.json_data.max_energy}\n", 1)

        return class_text

    def _indent(self, text: str, level: int) -> str:
        indent = '    ' * level
        return indent + text

    def _get_path(self) -> str:
        character_name = self._get_character_name()
        file_name = self._convert_camel_to_snake(character_name)
        return os.path.join('generated', 'character', f"{file_name}.py")

    def _get_character_name(self) -> str:
        if self.json_data.name == '{NICKNAME}':
            return f'Trailblazer{''.join(self.json_data.path.split())}'

        if self.json_data.name == 'March 7th':
            print(self.json_data.path)
            return f'March7th{''.join(self.json_data.path.split())}'

        # Remove special characters and convert to lowercase
        sanitized_name = ''.join(e for e in self.json_data.name if e.isalnum())
        sanitized_name = sanitized_name.replace(' ', '')
        return sanitized_name

    def _convert_camel_to_snake(self, name: str) -> str:
        return ''.join(['_' + i.lower() if i.isupper() else i for i in name]).lstrip('_')

    def serialize(self) -> None:
        preamble = self._get_preamble()
        class_definition = self._get_class_definition()
        class_attributes = self._get_basic_class_attributes()
        file_path = self._get_path()

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(preamble)
            f.write(class_definition)
            f.write(class_attributes)
            f.write("\n")

        print(f"Serialized {self.json_data.name} to {file_path}")


def serialize(file_path: str):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        character = CharacterOutput(**data)
        serializer = JsonClassSerializer(character)
        serializer.serialize()


def main():
    json_dir = pathlib.Path('./output/')
    json_files = list(json_dir.glob('*.json'))
    json_files.sort(key=lambda x: x.stem)  # Sort by filename without extension
    for path in json_files:
        serialize(str(path))


if __name__ == "__main__":
    main()
