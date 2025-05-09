from input_schema.base import InputSchemaBase


class LightConeSkillSchema(InputSchemaBase):

    skill_id: str
    skill_name: str
    skill_description: str
    _parameters: list[list]          # List of parameters, keyed by superimposition level
    _ability_properties: list[dict]  # List of ability properties, keyed by superimposition level

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