''' Script used as app entry point '''

import sys
import os
from songdatabase.config import init_config
from songdatabase.logger import init_logger
from songdatabase.database import init_database
from songdatabase.gui.main_window import init_main_window
from PyQt6.QtWidgets import QApplication

def start():
    config = init_config()
    loggers = init_logger(config)
    init_database(config, loggers['db_logger'])

    app = QApplication(sys.argv)
    main_window = init_main_window(app, config, loggers['window_logger'])
    main_window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    start()
