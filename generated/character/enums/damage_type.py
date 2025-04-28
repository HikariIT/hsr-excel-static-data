from enum import Enum


class DamageType(Enum):
    PHYSICAL = 'Physical'
    FIRE = 'Fire'
    ICE = 'Ice'
    LIGHTNING = 'Thunder'
    WIND = 'Wind'
    QUANTUM = 'Quantum'
    IMAGINARY = 'Imaginary'

    @classmethod
    def _get_from_string(cls, value: str) -> 'DamageType':
        for item in cls:
            if item.value == value:
                return item
        raise ValueError(f"'{value}' is not a valid {cls.__name__} value.")