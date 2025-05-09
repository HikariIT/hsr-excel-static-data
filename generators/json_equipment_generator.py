from input_schema.light_cone.promotion import LightConePromotionSchema
from input_schema.light_cone.light_cone import LightConeSchema
from input_schema.light_cone.skill import LightConeSkillSchema
from input_schema.db.database import Database

from image_downloaders.honey_hunter import HoneyHunterImporter
from generators.json_generator_base import FileParserBase
from constants.excel_files import ExcelOutputFile
from common.enum.rarity import Rarity


class LightConeParser(FileParserBase):

    DOWNLOAD_LIGHT_CONE_IMAGES = False  # Set to False to skip downloading images

    # Pair of (level, superimposition level), this overrides default '80/80' and S5 for 4-stars / S1 for 5-stars
    LIGHT_CONE_OVERRIDES = {

    }

    def __init__(self, lang: str = 'EN'):
        super().__init__(lang)
        self.honey_hunter_importer = HoneyHunterImporter()

    def parse_light_cones(self):
        for equipment_id in self.light_cones.get_ids():
            self.parse_light_cone(self.light_cones[equipment_id])

    def parse_light_cone(self, light_cone: LightConeSchema):
        skill = self.light_cone_skills_db[light_cone.skill_id]
        ascensions = self.light_cone_ascension[light_cone.equipment_id]

        if light_cone.name in self.LIGHT_CONE_OVERRIDES:
            level, superimposition_level = self.LIGHT_CONE_OVERRIDES[light_cone.name]
        else:
            level = '80/80'
            superimposition_level = 5 if light_cone.rarity == Rarity.FOUR_STAR else 1

        skill_description = skill.get_text_for_superimposition(superimposition_level)
        stats_for_levels = ascensions.get_stats_for_levels()
        stats = stats_for_levels[level]

        print('-' * 50)
        print(light_cone.name, level, f"S{superimposition_level}")
        print(f"Stats: {stats.hp:.0f} HP, {stats.atk:.2f} ATK, {stats.defence:.2f} DEF")
        print(f"Skill: {skill.skill_name}")
        print(f"Description: {skill_description}")

        if self.DOWNLOAD_LIGHT_CONE_IMAGES:
            self.honey_hunter_importer.download_light_cone_image(light_cone.name, light_cone.equipment_id)

        image_path = f'https://github.com/HikariIT/hsr-excel-static-data/tree/main/output/img/light-cone-icon/{light_cone.equipment_id}.webp'
        print(f"Image: {image_path}")

    def open(self):
        self._initialize_text_map()
        self._initialize_light_cones()
        self._initialize_light_cone_ascension()
        self._initialize_light_cone_skills()
        self._initialize_paths()

    def _initialize_light_cones(self):
        with open(self.EXCEL_OUTPUT_PATH / ExcelOutputFile.LIGHT_CONE_MAIN.value, 'r', encoding='utf-8') as file:
            self.light_cones = Database[LightConeSchema](file, LightConeSchema, 'EquipmentID')
            self.light_cones.load(self.text_map)
            self.logger.debug(f"Loaded light cone data: {len(self.light_cones.data)} entries")

    def _initialize_light_cone_ascension(self):
        with open(self.EXCEL_OUTPUT_PATH / ExcelOutputFile.LIGHT_CONE_ASCENSION.value, 'r', encoding='utf-8') as file:
            self.light_cone_ascension = Database[LightConePromotionSchema](file, LightConePromotionSchema, 'EquipmentID')
            self.light_cone_ascension.load(self.text_map)
            self.logger.debug(f"Loaded light cone ascension data: {len(self.light_cone_ascension.data)} entries")

    def _initialize_light_cone_skills(self):
        with open(self.EXCEL_OUTPUT_PATH / ExcelOutputFile.LIGHT_CONE_SKILLS.value, 'r', encoding='utf-8') as file:
            self.light_cone_skills_db = Database[LightConeSkillSchema](file, LightConeSkillSchema, 'SkillID')
            self.light_cone_skills_db.load(self.text_map)
            self.logger.debug(f"Loaded light cone skills data: {len(self.light_cone_skills_db.data)} entries")

