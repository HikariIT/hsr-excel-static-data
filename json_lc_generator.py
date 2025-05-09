from json_generator_base import FileParserBase
from excel_files import ExcelOutputFile
from schema.light_cones import Rarity
from pathlib import Path
import logging
import json

from input_schema.db.database import Database
from input_schema.light_cone.skill import LightConeSkillSchema
from input_schema.light_cone.promotion import LightConePromotionSchema

class LightConeParser(FileParserBase):

    def __init__(self, lang: str = 'EN'):
        super().__init__(lang)

    def parse_light_cones(self):
        print(self.light_cones[0])
        for light_cone in self.light_cones:
            self.parse_light_cone(light_cone)
            break

    def parse_light_cone(self, light_cone: dict):
        print('-' * 50)
        light_cone_id = light_cone['EquipmentID']
        name = self._unhash(light_cone['EquipmentName']['Hash'])
        path = self._get_path(light_cone['AvatarBaseType'])
        rarity = self._get_light_cone_rarity(light_cone['Rarity'])
        print(light_cone)

    def _get_skill(self, equipment_skill_id: str) -> dict:
        pass

    def _get_light_cone_rarity(self, rarity: str) -> Rarity:
        if rarity == 'CombatPowerLightconeRarity3':
            return Rarity.THREE_STAR
        elif rarity == 'CombatPowerLightconeRarity4':
            return Rarity.FOUR_STAR
        return Rarity.FIVE_STAR

    def open(self):
        self._initialize_text_map()
        self._initialize_light_cones()
        self._initialize_light_cone_ascension()
        self._initialize_light_cone_skills()
        self._initialize_paths()

    def _initialize_light_cones(self):
        with open(self.EXCEL_OUTPUT_PATH / ExcelOutputFile.LIGHT_CONE_MAIN.value, 'r', encoding='utf-8') as file:
            self.light_cones = json.load(file)
            self.logger.debug(f"Loaded light cone data: {len(self.light_cones)} entries")

    def _initialize_light_cone_ascension(self):
        with open(self.EXCEL_OUTPUT_PATH / ExcelOutputFile.LIGHT_CONE_ASCENSION.value, 'r', encoding='utf-8') as file:
            self.light_cone_ascension = Database(file, unique_key='EquipmentID', element_class=LightConePromotionSchema)
            self.light_cone_ascension.load(self.text_map)
            self.logger.debug(f"Loaded light cone ascension data: {len(self.light_cone_ascension.data)} entries")

    def _initialize_light_cone_skills(self):
        with open(self.EXCEL_OUTPUT_PATH / ExcelOutputFile.LIGHT_CONE_SKILLS.value, 'r', encoding='utf-8') as file:
            self.light_cone_skills_db = Database(file, unique_key='SkillID', element_class=LightConeSkillSchema)
            self.light_cone_skills_db.load(self.text_map)
            self.logger.debug(f"Loaded light cone skills data: {len(self.light_cone_skills_db.data)} entries")

if __name__ == '__main__':
    parser = LightConeParser(lang='EN')
    parser.open()
    parser.parse_light_cones()
