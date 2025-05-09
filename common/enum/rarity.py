from enum import Enum


class Rarity(Enum):
    FOUR_STAR = 4
    FIVE_STAR = 5
    THREE_STAR = 3
    TWO_STAR = 2
    ONE_STAR = 1

    @staticmethod
    def from_equipment_rarity_string(rarity_str: str) -> 'Rarity':
        """
        Convert a string to a Rarity enum member.
        :param rarity_str: The string representation of the rarity.
        :return: The corresponding Rarity enum member.
        """
        conversion_dict = {
            'CombatPowerLightconeRarity1': Rarity.ONE_STAR,
            'CombatPowerLightconeRarity2': Rarity.TWO_STAR,
            'CombatPowerLightconeRarity3': Rarity.THREE_STAR,
            'CombatPowerLightconeRarity4': Rarity.FOUR_STAR,
            'CombatPowerLightconeRarity5': Rarity.FIVE_STAR
        }
        try:
            return conversion_dict[rarity_str]
        except KeyError:
            raise ValueError(f"Invalid rarity string: {rarity_str}. Valid options are: {list(conversion_dict.keys())}.")