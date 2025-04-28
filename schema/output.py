from dataclasses import dataclass
from enum import Enum


class Stat(Enum):
    HP = 'HP'
    ATK = 'ATK'
    DEF = 'DEF'
    SPD = 'SPD'


class DamageType(Enum):
    PHYSICAL = 'Physical'
    FIRE = 'Fire'
    ICE = 'Ice'
    LIGHTNING = 'Lightning'
    WIND = 'Wind'
    QUANTUM = 'Quantum'
    IMAGINARY = 'Imaginary'


class SkillType(Enum):
    NORMAL = 'Normal'
    ULTIMATE = 'Ultimate'
    TALENT = 'Talent'
    SKILL = 'BPSkill'
    TECHNIQUE = 'Technique'


@dataclass
class CharacterBaseStats:
    hp: float
    atk: float
    defense: float
    spd: float
    crit_rate: float
    crit_dmg: float

@dataclass
class CharacterOutput:
    id: str
    name: str
    rarity: int
    path: str
    damage_type: str
    skills: dict[str, 'CharacterSkill']
    major_traces: dict[str, 'CharacterMajorTrace']
    minor_traces: dict[str, 'CharacterMinorTrace']
    max_energy: int | None
    stats: dict[str, 'CharacterBaseStats']
    unreleased: bool


@dataclass
class CharacterMinorTrace:
    id: str
    stat: str
    value: int
    required_level: int | None
    required_ascension: int | None
    prerequsite_traces: list[str]
    children: list['CharacterMinorTrace']


@dataclass
class CharacterSkillTrace:
    id: str
    max_level: int
    related_skill_id: str


@dataclass
class CharacterMajorTrace:
    id: str
    required_ascension: int | None
    prerequsite_traces: list[str]
    children: list['CharacterMajorTrace']
    params: list[int]

@dataclass
class CharacterSkill:
    id: str
    name: str
    max_level: int
    damage_type: DamageType | str
    type: SkillType
    type_text: str
    effect: str
    effect_text: str
    simple_description: str
    full_description: str
    params: list[list[int]]


