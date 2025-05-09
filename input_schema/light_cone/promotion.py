from input_schema.base import InputSchemaBase
from utils.base_stats import BaseStats


class LightConePromotionSchema(InputSchemaBase):

    equipment_id: str
    promotion_level: list[int]
    max_level: list[int]
    base_stats: list[BaseStats]
    scaling_stats: list[BaseStats]

    MAX_ASCENSION_LEVEL: int = 6

    def __init__(self, text_map: dict[str, str]):
        super().__init__(text_map)
        self.promotion_level = [i  for i in range(self.MAX_ASCENSION_LEVEL + 1)]
        self.max_level = [0] * (self.MAX_ASCENSION_LEVEL + 1)
        self.base_stats = [BaseStats() for _ in range(self.MAX_ASCENSION_LEVEL + 1)]
        self.scaling_stats = [BaseStats() for _ in range(self.MAX_ASCENSION_LEVEL + 1)]

    def update(self, schema: dict) -> None:
        if not hasattr(self, 'equipment_id'):
            self.equipment_id = schema['EquipmentID']

        if 'Promotion' in schema:
            promotion = schema['Promotion']
            if promotion < 1 or promotion > self.MAX_ASCENSION_LEVEL:
                raise ValueError(f"Invalid ascension level: {schema['Promotion']}")
        else:
            promotion = 0

        self.base_stats[promotion] = BaseStats(
            schema['BaseHP']['Value'],
            schema['BaseAttack']['Value'],
            schema['BaseDefence']['Value'],
        )

        self.scaling_stats[promotion] = BaseStats(
            schema['BaseHPAdd']['Value'],
            schema['BaseAttackAdd']['Value'],
            schema['BaseDefenceAdd']['Value'],
        )

        self.max_level[promotion] = schema['MaxLevel']