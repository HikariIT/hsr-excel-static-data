import pandas as pd
import json
import os

from schema.output import CharacterBaseStats, CharacterOutput


class ExcelDataTransformer:

    CHARACTER_DATA_DIRECTORY = 'output'
    ABSOULUTE_ICON_DIRECTORY = r'D:\HSR\turnbasedgamedata\scripts\output\img'

    def __init__(self):
        self._character_files = self._get_character_files()
        columns = ['Image', 'Name', 'Element', 'Path', 'Base HP', 'Base ATK', 'Base DEF', 'Base SPD',
                   'HP%', 'ATK%', 'DEF%', 'CRIT Rate', 'CRIT DMG', 'Effect Hit Rate',
                   'Effect RES', 'BE%', 'DMG%', 'ERR%',
                   'OHB%', 'SPD', 'Max Energy', 'Icon Link']
        self._character_dataframe = pd.DataFrame({
            col: [] for col in columns
        })

        self._parse_character_files()
        self._character_dataframe = self._character_dataframe.reset_index(drop=True)
        self._character_dataframe = self._character_dataframe.drop_duplicates(subset=['Name'], keep='last')
        self._character_dataframe.to_excel('output/characters.xlsx', index=False, engine='openpyxl')

    def _get_character_files(self):
        with os.scandir(self.CHARACTER_DATA_DIRECTORY) as entries:
            return [entry.path for entry in entries if entry.is_file() and entry.name.endswith('.json')]

    def _parse_character_files(self):
        for file_path in self._character_files:
            self._parse_character_file(file_path)

    def _parse_character_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            str_data = file.read()
            data = json.loads(str_data)
            character_data = CharacterOutput(**data)
            base_stats = self._get_base_stats(character_data)
            minor_trace_stats = self._get_stats_from_minor_traces(character_data)

            character_df = pd.DataFrame({
                'Image': [''],
                'Name': [self._get_character_name(character_data)],
                'Element': [character_data.damage_type],
                'Path': [character_data.path],
                'Base HP': [base_stats['Base HP']],
                'Base ATK': [base_stats['Base ATK']],
                'Base DEF': [base_stats['Base DEF']],
                'Base SPD': [base_stats['Base SPD']],
                'HP%': [self._get_stat(minor_trace_stats, 'HPAddedRatio')],
                'ATK%': [self._get_stat(minor_trace_stats, 'AttackAddedRatio')],
                'DEF%': [self._get_stat(minor_trace_stats, 'DefenceAddedRatio')],
                'CRIT Rate': [self._get_stat(minor_trace_stats, 'CriticalChanceBase')],
                'CRIT DMG': [self._get_stat(minor_trace_stats, 'CriticalDamageBase')],
                'Effect Hit Rate': [self._get_stat(minor_trace_stats, 'Effect Hit Rate')],
                'Effect RES': [self._get_stat(minor_trace_stats, 'StatusResistanceBase')],
                'BE%': [self._get_stat(minor_trace_stats, 'BreakDamageAddedRatioBase')],
                'DMG%': [self._get_stat(minor_trace_stats, f'{character_data.damage_type}AddedRatio')],
                'ERR%': [''],
                'OHB%': [''],
                'SPD': [self._get_stat(minor_trace_stats, 'SpeedDelta')],
                'Max Energy': [character_data.max_energy if character_data.max_energy else ''],
                'Icon Link': [os.path.join(self.ABSOULUTE_ICON_DIRECTORY, self._get_img_link(character_data))]
            })

            # Add the character dataframe to the main dataframe
            self._character_dataframe = pd.concat([self._character_dataframe, character_df], ignore_index=True)

    def _get_character_name(self, character_data: CharacterOutput):
        if character_data.id in ['8001', '8002']:
            return 'Trailblazer (Destruction)'
        elif character_data.id in ['8003', '8004']:
            return 'Trailblazer (Preservation)'
        elif character_data.id in ['8005', '8006']:
            return 'Trailblazer (Harmony)'
        elif character_data.id in ['8007', '8008']:
            return 'Trailblazer (Remembrance)'
        if character_data.name == 'March 7th':
            return f'March 7th ({character_data.path})'
        return character_data.name

    def _get_img_link(self, character_data: CharacterOutput):
        return os.path.join(self.ABSOULUTE_ICON_DIRECTORY, f'wait-icon\\{character_data.id}.webp')

    def _get_base_stats(self, character_data: CharacterOutput):
        base_stats = CharacterBaseStats(**character_data.stats['80/80'])
        return {
            'Base HP': round(base_stats.hp, 3),
            'Base ATK': round(base_stats.atk, 3),
            'Base DEF': round(base_stats.defense, 3),
            'Base SPD': round(base_stats.spd, 3),
        }

    def _get_stats_from_minor_traces(self, character_data: CharacterOutput):
        stats = {}
        for trace in character_data.minor_traces.values():
            if trace['stat']:
                if trace['stat'] in stats:
                    stats[trace['stat']] += trace['value']
                else:
                    stats[trace['stat']] = trace['value']
        return stats

    def _get_stat(self, stats_from_minor_traces: dict, stat_name: str):
        return stats_from_minor_traces.get(stat_name, '')

if __name__ == "__main__":
    transformer = ExcelDataTransformer()
