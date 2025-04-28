from dataclasses import asdict
import random
import time
from schema.output import CharacterMajorTrace, CharacterOutput, CharacterMinorTrace, CharacterSkillTrace, CharacterSkill, CharacterBaseStats
from excel_files import ExcelOutputFile
from pathlib import Path
from enum import Enum
import logging
import requests
import json


class CharacterRarityHSRInternal(str, Enum):
    FOUR_STAR = 'CombatPowerAvatarRarityType4'
    FIVE_STAR = 'CombatPowerAvatarRarityType5'


class FileParser:

    EXCEL_OUTPUT_PATH = Path('../ExcelOutput')
    TEXT_MAPS_PATH = Path('../TextMap')
    main_avatar_file: dict[int, dict]
    character_traces: dict[int, list[dict]]

    def __init__(self, lang: str = 'EN'):
        self.lang = lang
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    def parse_character(self, character_id: int) -> None:
        character_main = self.main_avatar_file[character_id]

        avatar_name_hash = character_main['AvatarName']['Hash']
        self.logger.info(f'Parsing character with ID {character_id}: {self._unhash(avatar_name_hash)}')
        rarity = 5 if character_main['Rarity'] == CharacterRarityHSRInternal.FIVE_STAR else 4

        character_data = CharacterOutput(
            id=str(character_id),
            name=self._unhash(avatar_name_hash),
            rarity=rarity,
            path=self._get_path(character_main['AvatarBaseType']),
            damage_type=character_main['DamageType'],
            skills={},
            major_traces={},
            minor_traces={},
            max_energy=character_main.get('SPNeed', {'Value': None})['Value'],
            stats={},
            unreleased=False
        )

        all_traces = self._parse_traces(character_id)
        skill_traces = {trace_id: trace for trace_id, trace in all_traces.items() if isinstance(trace, CharacterSkillTrace)}
        skills = self._parse_skills(skill_traces)
        stats = self._parse_stats(character_id)

        character_data.stats = stats
        character_data.skills = skills
        character_data.major_traces = {trace_id: trace for trace_id, trace in all_traces.items() if isinstance(trace, CharacterMajorTrace)}
        character_data.minor_traces = {trace_id: trace for trace_id, trace in all_traces.items() if isinstance(trace, CharacterMinorTrace)}

        with open(f'output/{character_id}.json', 'w') as file:
            json.dump(asdict(character_data), file, indent=2)

    def _save_optional_image(self, character_data: CharacterOutput) -> None:
        name_sanitized = self._get_honey_hunter_name(character_data)
        action_img_wait_icon = f'https://starrail.honeyhunterworld.com/img/character/{name_sanitized}_wait_icon.webp'

        request = requests.get(action_img_wait_icon)
        if request.status_code == 200:
            with open(f'output/img/wait-icon/{character_id}.webp', 'wb') as file:
                file.write(request.content)
            self.logger.info(f"Downloaded image for character ID {character_id} to output/img/wait-icon/{character_id}.webp")
        else:
            self.logger.warning(f"Failed to download image for character ID {character_id}")

        time.sleep(random.uniform(1, 4))

    def _get_honey_hunter_name(self, character_data: CharacterOutput) -> str:
        if character_data.name == '{NICKNAME}':
            trailblazer_id = character_data.id[1:].lstrip('0')
            if trailblazer_id == '1':
                return 'trailblazer-character'
            return f'trailblazer-character-{trailblazer_id}'
        if character_data.name == 'March 7th':
            if character_data.path == 'Preservation':
                return 'march-7th-character'
            if character_data.path == 'The Hunt':
                return 'march-7th-character-2'
        name_sanitized = ''.join(filter(str.isalnum, character_data.name))
        name_sanitized = ''.join(['-' + i.lower() if i.isupper() else i for i in name_sanitized]).lstrip('-')
        return f'{name_sanitized}-character'

    def _unhash(self, hash_value: int) -> str:
        return self.text_map.get(str(hash_value))

    def _get_path(self, path_id: str) -> str:
        return self.class_to_path.get(path_id, 'General')

    def get_all_character_ids(self) -> list[int]:
        return list(self.main_avatar_file.keys())

    def open(self):
        with open(self.EXCEL_OUTPUT_PATH / ExcelOutputFile.AVATAR_MAIN.value, 'r', encoding='utf-8') as file:
            main_avatar_json = json.load(file)
            self.main_avatar_file = {character['AvatarID']: character for character in main_avatar_json}

        with open(self.TEXT_MAPS_PATH / f'TextMap{self.lang}.json', 'r', encoding='utf-8') as file:
            self.text_map = json.load(file)
            self.logger.debug(f"Loaded text map for language {self.lang}: {len(self.text_map)} entries")

        with open(self.EXCEL_OUTPUT_PATH / ExcelOutputFile.AVATAR_PATHS.value, 'r', encoding='utf-8') as file:
            path_list = json.load(file)
            self.class_to_path = {}
            for path in path_list:
                if 'ID' not in path:
                    continue
                self.class_to_path[path['ID']] = self._unhash(path['BaseTypeText']['Hash'])
            self.logger.debug(f"Loaded paths: {self.class_to_path}")

        with open(self.EXCEL_OUTPUT_PATH / ExcelOutputFile.AVATAR_TRACES.value, 'r', encoding='utf-8') as file:
            self.traces_list = json.load(file)
            self.logger.debug(f"Loaded traces: {len(self.traces_list)} entries")
            self._prepare_traces()
            self.logger.debug(f"Prepared traces for {len(self.character_traces)} characters")

        with open(self.EXCEL_OUTPUT_PATH / ExcelOutputFile.AVATAR_SKILLS.value, 'r', encoding='utf-8') as file:
            self.skills_list = json.load(file)

        with open(self.EXCEL_OUTPUT_PATH / ExcelOutputFile.AVATAR_MEMOSPRITE_SKILLS.value, 'r', encoding='utf-8') as file:
            self.skills_list.extend(json.load(file))
            self.logger.debug(f"Loaded skills: {len(self.skills_list)} entries")
            self._prepare_skills()
            self.logger.debug(f"Loaded {len(self.character_skills)} skills")

        with open(self.EXCEL_OUTPUT_PATH / ExcelOutputFile.AVATAR_ASCENSION.value, 'r', encoding='utf-8') as file:
            self.ascension_list = json.load(file)
            self._prepare_stats()

    def _prepare_traces(self):
        self.character_traces = {}
        for trace in self.traces_list:
            if 'AvatarID' not in trace:
                continue
            character_id = trace['AvatarID']
            self.character_traces.setdefault(character_id, []).append(trace)

    def _prepare_skills(self):
        self.character_skills = {}
        for skill in self.skills_list:
            skill_id = skill['SkillID']
            self.character_skills.setdefault(str(skill_id), []).append(skill)

    def _prepare_stats(self):
        self.character_ascensions = {}
        for ascension in self.ascension_list:
            if 'AvatarID' not in ascension:
                continue
            character_id = str(ascension['AvatarID'])
            self.character_ascensions.setdefault(character_id, []).append(ascension)

    def _parse_traces(self, character_id: int) -> dict[str, CharacterMajorTrace | CharacterMinorTrace | CharacterSkillTrace]:
        if character_id not in self.character_traces:
            self.logger.warning(f"No traces found for character ID {character_id}")
            return {}

        traces = self.character_traces[character_id]

        stat_traces = list(filter(lambda trace: len(trace['StatusAddList']) != 0, traces))
        skill_traces = list(filter(lambda trace: len(trace['StatusAddList']) == 0, traces))

        traces = {}

        for trace in skill_traces:
            if trace['LevelUpSkillID'] is None or len(trace['LevelUpSkillID']) == 0:
                # Handle a major trace
                parsed_trace = CharacterMajorTrace(
                    id=str(trace['PointID']),
                    required_ascension=trace.get('AvatarPromotionLimit'),
                    prerequsite_traces=trace['PrePoint'],
                    children=[],
                    params=[param['Value'] for param in trace['ParamList']],
                )
                traces[parsed_trace.id] = parsed_trace
                for parent in parsed_trace.prerequsite_traces:
                    if str(parent) in traces:
                        traces[str(parent)].children.append(parsed_trace.id)
                continue

            # Handle a regular skill trace
            parsed_trace = CharacterSkillTrace(
                id=str(trace['PointID']),
                max_level=trace['MaxLevel'],
                related_skill_id=str(trace['LevelUpSkillID'][0]),
            )
            traces[parsed_trace.id] = parsed_trace

        for trace in stat_traces:
            add_list = trace['StatusAddList'][0]
            parsed_trace = CharacterMinorTrace(
                id=str(trace['PointID']),
                stat=add_list['PropertyType'],
                value=add_list['Value']['Value'],
                required_level=trace.get('AvatarLevelLimit', ''),
                required_ascension=trace.get('AvatarPromotionLimit', ''),
                prerequsite_traces=trace['PrePoint'],
                children=[],
            )
            traces[parsed_trace.id] = parsed_trace
            for parent in parsed_trace.prerequsite_traces:
                if str(parent) in traces:
                    traces[str(parent)].children.append(parsed_trace.id)

        return traces

    def _parse_skills(self, traces: dict[str, CharacterSkillTrace]) -> dict[str, CharacterSkill]:
        skills = {}

        for skill in traces.values():
            skill_data_list = self.character_skills[skill.related_skill_id]
            skill_data = skill_data_list[0]
            skills[skill.related_skill_id] = CharacterSkill(
                id=skill.related_skill_id,
                name=self._unhash(skill_data['SkillName']['Hash']),
                max_level=len(skill_data_list),
                damage_type=skill_data.get('StanceDamageType', ''),
                type=skill_data.get('AttackType', ''),
                type_text=self._unhash(skill_data['SkillTypeDesc']['Hash']),
                effect=skill_data['SkillEffect'],
                effect_text=skill_data['SkillEffect'],
                simple_description=self._unhash(skill_data['SimpleSkillDesc']['Hash']),
                full_description=self._unhash(skill_data['SkillDesc']['Hash']),
                params=[],
            )

            for skill_data in skill_data_list:
                skills[skill.related_skill_id].params.append([param['Value'] for param in skill_data['ParamList']])

        return skills

    def _parse_stats(self, character_id: int) -> dict[str, CharacterBaseStats]:
        ascensions = self.character_ascensions[str(character_id)]
        current_level = 1
        stats_for_level = {}

        for ascension in ascensions:
            for lvl in range(current_level, ascension['MaxLevel'] + 1):
                level_name = f'{lvl}/{ascension['MaxLevel']}'
                stats_for_level[level_name] = CharacterBaseStats(
                    hp=ascension['HPBase']['Value'] + ascension['HPAdd']['Value'] * (lvl - 1),
                    atk=ascension['AttackBase']['Value'] + ascension['AttackAdd']['Value'] * (lvl - 1),
                    defense=ascension['DefenceBase']['Value'] + ascension['DefenceAdd']['Value'] * (lvl - 1),
                    spd=ascension['SpeedBase']['Value'],
                    crit_rate=ascension['CriticalChance']['Value'],
                    crit_dmg=ascension['CriticalDamage']['Value']
                )
            current_level = ascension['MaxLevel']

        return stats_for_level

if __name__ == '__main__':
    file_parser = FileParser()
    file_parser.open()
    for character_id in file_parser.get_all_character_ids():
        file_parser.parse_character(character_id)