from enum import Enum


class Path(Enum):
    PRESERVATION = 'Preservation'
    DESTRUCTION = 'Destruction'
    THE_HUNT = 'The Hunt'
    NIHILITY = 'Nihility'
    ERUDITION = 'Erudition'
    HARMONY = 'Harmony'
    ABUNDANCE = 'Abundance'
    REMEMBRANCE = 'Remembrance'

    @classmethod
    def _get_from_string(cls, value: str) -> 'Path':
        for item in cls:
            if item.value == value:
                return item
        raise ValueError(f"'{value}' is not a valid {cls.__name__} value.")