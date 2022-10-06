
import yaml 
import os

# replace $USER with actual user, why tf is snakemake not doing this

with open("config.yaml", "r") as inh:
    config = yaml.safe_load(inh)
new_config = {}


def expandcheck(x):
    if type(x) is str:
        x = os.path.expandvars(x)
    return x


for k, v in config.items():
    v = expandcheck(v)
    if type(v) is list:
        new_list = []
        for elem in v:
            elem = expandcheck(elem)
            new_list.append(elem)
        v = new_list
    new_config[k] = v

with open("config.yaml", "w") as outh:
    yaml.dump(new_config, outh)
