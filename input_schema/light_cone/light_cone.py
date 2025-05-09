from input_schema.base import InputSchemaBase
from common.enum.rarity import Rarity
from common.enum.path import Path


class LightConeSchema(InputSchemaBase):

    equipment_id: int       # Key: (LightConeSchema) equipment_id
    skill_id: int           # Foreign Key: (LightConeSkillSchema) skill_id
    released: bool
    rarity: Rarity
    path: Path
    name: str

    def __init__(self, text_map: dict[str, str]):
        super().__init__(text_map)

    def update(self, schema: dict) -> None:
        self.equipment_id = schema['EquipmentID']
        self.skill_id = schema['SkillID']
        self.released = schema['Release']
        self.rarity = Rarity.from_equipment_rarity_string(schema['Rarity'])
        self.path = Path.from_string(schema['AvatarBaseType'])
        self.name = self._unhash(schema['EquipmentName']['Hash'])