import json

config_file = "configuration_files/calibration_configuration.json"

def add_calibration_point(name, co):
    with open(config_file, 'r+') as f:
        data = json.load(f)
        data['points'][name] = co
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()

def remove_calibration_point(name):
    with open(config_file, 'r+') as f:
        data = json.load(f)
        data['points'].pop(name, None)
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()

def get_calibration_points():
    with open(config_file, 'r') as f:
        data = json.load(f)
        return data['points']

