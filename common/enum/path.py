from enum import Enum


class Path(Enum):
    DESTRUCTION = 'Destruction'
    THE_HUNT = 'The Hunt'
    ERUDITION = 'Erudition'
    HARMONY = 'Harmony'
    NIHILITY = 'Nihility'
    PRESERVATION = 'Preservation'
    ABUNDANCE = 'Abundance'
    REMEMBRANCE = 'Remembrance'

    @staticmethod
    def from_string(path_str: str) -> 'Path':
        """
        Convert a string to a Path enum member.
        :param path_str: The string representation of the path.
        :return: The corresponding Path enum member.
        """
        conversion_dict = {
            'Warrior': Path.DESTRUCTION,
            'Rogue': Path.THE_HUNT,
            'Mage': Path.ERUDITION,
            'Shaman': Path.HARMONY,
            'Warlock': Path.NIHILITY,
            'Knight': Path.PRESERVATION,
            'Priest': Path.ABUNDANCE,
            'Memory': Path.REMEMBRANCE
        }
        try:
            return conversion_dict[path_str]
        except KeyError:
            raise ValueError(f"Invalid path string: {path_str}. Valid options are: {list(conversion_dict.keys())}.")