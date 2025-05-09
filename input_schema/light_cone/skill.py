from input_schema.base import InputSchemaBase
from typing import Callable
import re


class LightConeSkillSchema(InputSchemaBase):

    skill_id: int                    # Key: (LightConeSkillSchema) skill_id
    skill_name: str
    skill_description: str
    _parameters: list[list]          # Index: superimposition level
    _ability_properties: list[dict]  # Index: superimposition level

    MAX_SUPERIMPOSITION_LEVEL: int = 5

    def __init__(self, text_map: dict[str, str]):
        super().__init__(text_map)
        self._parameters = [[] for _ in range(self.MAX_SUPERIMPOSITION_LEVEL)]
        self._ability_properties = [{} for _ in range(self.MAX_SUPERIMPOSITION_LEVEL)]

    def update(self, schema: dict) -> None:
        if len(self._parameters[0]) == 0:
            self.skill_id = schema['SkillID']
            self.skill_name = self._unhash(schema['SkillName']['Hash'])
            self.skill_description = self._unhash(schema['SkillDesc']['Hash'])

        level = schema['Level'] - 1
        if level < 0 or level >= self.MAX_SUPERIMPOSITION_LEVEL:
            raise ValueError(f"Invalid superimposition level: {level + 1}")

        self._parameters[level] = [param['Value'] for param in schema['ParamList']]
        self._ability_properties[level] = {param['PropertyType']: param['Value']['Value'] for param in schema['AbilityProperty']}

    def get_text_for_superimposition(self, superimposition_level: int) -> str:
        if superimposition_level < 1 or superimposition_level > self.MAX_SUPERIMPOSITION_LEVEL:
            raise ValueError(f"Invalid superimposition level: {superimposition_level}")

        skill_description = self.skill_description
        pattern = re.compile(r'(?:<color=.*?>)?<unbreak>#(?P<number>\d+)\[(?P<format>[^\]]+)\](?P<percent>%?)</unbreak>(?:</color>)?')
        return pattern.sub(self._sub_method_generator(superimposition_level), skill_description).replace('\\n', '\n')

    def _sub_method_generator(self, superimposition_level: int) -> Callable[[re.Match], str]:
        parameters = self._parameters[superimposition_level - 1]

        def _replace_match_in_description(match: re.Match) -> str:
            number = int(match.group("number"))
            format_str = match.group("format")
            has_percent = bool(match.group("percent"))

            parameter_value = parameters[number - 1]
            if format_str == 'i':
                if has_percent:
                    parameter_value *= 100
                    return f'{parameter_value:.0f}' + '%'
                return str(parameter_value)
            elif format_str == 'f1':
                if has_percent:
                    parameter_value *= 100
                    return f"{parameter_value:.1f}" + '%'
                return f"{parameter_value:.1f}"
            elif format_str == 'f2':
                if has_percent:
                    parameter_value *= 100
                    return f"{parameter_value:.2f}" + '%'
                return f"{parameter_value:.2f}"
            else:
                raise ValueError(f"Unknown format: {format_str}")

        return _replace_match_in_description