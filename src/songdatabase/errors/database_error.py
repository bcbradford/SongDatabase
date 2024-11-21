''' Module containing the database's error classes '''

class DatabaseError(Exception):

    def __init__(self, error_type="DatabaseError", description="Unhandled Error", logger_output=None):
        super().__init__(description)
        self._error_type = error_type
        self._logger_output = logger_output

    def to_string(self):
        return f"{self._error_type}: {self.args[0]}"

    def get_logger_output(self):
        return self._logger_output

class DatabaseInitError(Exception):
    def __init__(self, description, logger_output=None):
        super().__init__("DatabaseInitError", description, logger_output)

class DatabaseConnectionError(Exception):
    def __init__(self, description, logger_output=None):
        super().__init__("DatabaseConnectionError", description, logger_output)

class DatabaseQueryError(Exception):
    def __init__(self, description, logger_output=None):
        super().__init__("DatabaseQueryError", description, logger_output)
