import configparser
from generation import main

if __name__ == '__main__':
    # read parameters from .ini file
    config = configparser.ConfigParser()
    config.read('parameters.ini')

    SEED = int(config['GENERATION']['SEED'])  # for reproducibility
    NROWS = int(config['GENERATION']['NROWS'])
    NCOLS = int(config['GENERATION']['NCOLS'])
    NOBSTACLES = int(config['GENERATION']['NOBSTACLES'])
    AGGLOMERATION_FACTOR = float(config['GENERATION']['AGGLOMERATION_FACTOR'])

    PI_LENGTH = int(config['EXISTING_AGENTS']['PI_LENGTH'])  # constant length of the Pi route of the existing agents
    NAGENTS = int(config['EXISTING_AGENTS']['NAGENTS'])

    MAX = int(config['ENTRY_AGENT']['MAX'])  # maximum length of the route of the entry agent
    INITX = int(config['ENTRY_AGENT']['INITX'])  # initial x position of the entry agent
    INITY = int(config['ENTRY_AGENT']['INITY'])  # initial y position of the entry agent
    GOALX = int(config['ENTRY_AGENT']['GOALX'])  # goal x position of the entry agent
    GOALY = int(config['ENTRY_AGENT']['GOALY'])  # goal y position of the entry agent

    grid, agents = main.generate_instance(NROWS, NCOLS, NOBSTACLES, AGGLOMERATION_FACTOR, PI_LENGTH, NAGENTS, SEED)
