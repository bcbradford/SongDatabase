''' Module used to initialize the app's logger '''

import logging

def init_logger(config: dict) -> dict:
    loggers = {}

    for logger_name, logger_dict in config['logger'].items():
    
        logger = logging.getLogger(logger_dict['name'])
        
        if config['debug']: logger.setLevel(logging.DEBUG)
        else: logger.setLevel(logging.WARNING)

        info_handler = logging.FileHandler(logger_dict['info_log'])
        info_handler.setLevel(logging.INFO)
        error_handler = logging.FileHandler(logger_dict['error_log'])
        error_handler.setLevel(logging.ERROR)

        formatter = logging.Formatter(logger_dict['format'])
        info_handler.setFormatter(formatter)
        error_handler.setFormatter(formatter)

        logger.addHandler(info_handler)
        logger.addHandler(error_handler)

        loggers[logger_name] = logger

    return loggers
