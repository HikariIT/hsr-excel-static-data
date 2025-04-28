# This file is auto-generated. Do not edit.

from _character_base import CharacterBase
from enums.rarity import Rarity
from enums.path import Path
from enums.damage_type import DamageType


class Blade(CharacterBase):
    id: str = '1205'
    name: str = 'Blade'
    rarity: Rarity = Rarity.FIVE_STAR
    path: Path = Path.DESTRUCTION
    damage_type: DamageType = DamageType.WIND
    max_energy: int = 130

