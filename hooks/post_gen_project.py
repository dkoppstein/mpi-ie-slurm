
import yaml 
import os

# replace $USER with actual user, why tf is snakemake not doing this

with open("config.yaml", "r") as inh:
    config = yaml.safe_load(inh)
new_config = {}

for k, v in config.items():
    if type(v) is str:
        v = os.path.expandvars(v)
    new_config[k] = v

with open("config.yaml", "w") as outh:
    yaml.dump(new_config, outh)
