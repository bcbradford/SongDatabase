''' Script used as app entry point '''

import sys
import os
import asyncio
from songdatabase.config import init_config
from songdatabase.logger import init_logger
from songdatabase.database import init_database
from songdatabase.gui.main_window import init_main_window
from songdatabase.errors.database_error import *
from songdatabase.errors.app_error import *
from PyQt6.QtWidgets import QApplication

def start():
    print("Loading App")

    config = init_config()
    loggers = init_logger(config)

    try:
        db = init_database(config, loggers['db_logger'])
    except DatabaseInitError as e:
        print(e.to_string())
        loggers['db_logger'].error(e.get_logger_output())
        return

    app = QApplication(sys.argv)
    main_window = init_main_window(app, config, loggers['window_logger'], db)
    
    if main_window is None: return

    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    start()
