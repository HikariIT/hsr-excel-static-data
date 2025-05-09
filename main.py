from generators.json_equipment_generator import LightConeParser


if __name__ == '__main__':
    parser = LightConeParser(lang='EN')
    parser.open()
    parser.parse_light_cones()