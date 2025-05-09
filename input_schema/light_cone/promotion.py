from input_schema.base import InputSchemaBase
from common.base_stats import BaseStats


class LightConePromotionSchema(InputSchemaBase):

    equipment_id: int               # Foreign Key: (LightConeSchema) equipment_id
    promotion_level: list[int]      # Index: ascension level
    max_level: list[int]            # Index: ascension level
    base_stats: list[BaseStats]     # Index: ascension level
    scaling_stats: list[BaseStats]  # Index: ascension level

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

    def get_stats_for_levels(self) -> dict[str, BaseStats]:
        stats_for_levels = {}
        min_level = 1
        for i in range(self.MAX_ASCENSION_LEVEL + 1):
            max_level = self.max_level[i]
            for level in range(min_level, max_level + 1):
                base_stats = self.base_stats[i]
                scaling_stats = self.scaling_stats[i]
                stats_for_levels[f'{level}/{max_level}'] = BaseStats(
                    base_stats.hp + scaling_stats.hp * (level - 1),
                    base_stats.atk + scaling_stats.atk * (level - 1),
                    base_stats.defence + scaling_stats.defence * (level - 1)
                )

            min_level = max_level
        return stats_for_levels