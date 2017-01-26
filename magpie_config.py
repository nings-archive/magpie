'''
magpie_config
'''

import os, sys, json

# CONSTANTS
PATH_SCRIPT = sys.path[0] + '/'
PATH_CONFIG = PATH_SCRIPT + 'config.json'

def load():
    with open(PATH_CONFIG, 'r') as file:
        return json.loads(file.read())

def save(config_dict):
    with open(PATH_CONFIG, 'w') as file:
        json.dump(config_dict, file, indent=4)

if __name__ == '__main__':
    if not os.path.isfile(PATH_CONFIG):
        # init config with required info
        pass
    else:
        # add things
        pass
