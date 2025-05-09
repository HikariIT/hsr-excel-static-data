class BaseStats:
    def __init__(self, base_hp: float = 0, base_atk: float = 0, base_defence: float = 0):
        self.hp = base_hp
        self.atk = base_atk
        self.defence = base_defence

    def __mul__(self, other):
        if isinstance(other, float):
            return BaseStats(
                self.hp * other,
                self.atk * other,
                self.defence * other
            )
        elif isinstance(other, int):
            return BaseStats(
                self.hp * other,
                self.atk * other,
                self.defence * other
            )
        return NotImplemented

    def __add__(self, other):
        if isinstance(other, BaseStats):
            return BaseStats(
                self.hp + other.hp,
                self.atk + other.atk,
                self.defence + other.defence
            )
        return NotImplemented

