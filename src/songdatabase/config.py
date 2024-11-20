''' Loads the config.yml file into thte app's config dictionary. '''

import os
import yaml

def init_config() -> dict:
    package_path = os.path.dirname(os.path.dirname(__file__)) #src
    project_path = os.path.dirname(package_path) # SongDatabase
    config_path = os.path.join(project_path, "config.yml")

    if not os.path.exists(config_path):
        msg = f"Path: {os.path.join(SongDatabase, config_path)} not found"
        raise FileNotFoundError(msg)

    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)

    if not config:
        raise ValueError(f"Failed to load configuration file.")

    # Set Database Path
    database_path = config['db_path']
    database = config['database']
    config['database'] = os.path.join(project_path, database_path, database)

    # Set Logger Paths
    log_path = config['log_path']

    info_log = config['logger']['info_log']
    info_path = os.path.join(project_path, log_path, info_log)
    config['logger']['info_log'] = info_path

    error_log = config['logger']['error_log']
    error_path = os.path.join(project_path, log_path, error_log)
    config['logger']['error_log'] = error_path

    return config

