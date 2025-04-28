# This file is auto-generated. Do not edit.

from _character_base import CharacterBase
from enums.rarity import Rarity
from enums.path import Path
from enums.damage_type import DamageType


class Serval(CharacterBase):
    id: str = '1103'
    name: str = 'Serval'
    rarity: Rarity = Rarity.FOUR_STAR
    path: Path = Path.ERUDITION
    damage_type: DamageType = DamageType.LIGHTNING
    max_energy: int = 100

