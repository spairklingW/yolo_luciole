import yaml


def dump_yaml(data, file_path):
    with open(file_path, 'w') as outfile:
        yaml.dump(data, outfile, default_flow_style=False)