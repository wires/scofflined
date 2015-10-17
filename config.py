import yaml

with open("config.yaml", "r") as f:
    config = yaml.load(f)

auth = config['auth']
