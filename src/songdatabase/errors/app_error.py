''' Module containing the app's errors '''

class AppError(Exception):

    def __init__(self, error_type="AppError", description="Unhandled Error", logger_output=None):
        super().__init__(description)
        self._error_type = error_type
        self._logger_output = logger_output

    def to_stirng(self):
        return f"{self._error_type}: {self.Args[0]}"

    def get_logger_output(self):
        return self._logger_output


class AppLoadError(AppError):
    def __init__(self, description, logger_output=None):
        super().__init__("AppLoadError", description, logger_output)

class InputValidationError(AppError):
    def __init__(self, description, logger_output=None):
        super().__init__("InputValidationError", description, logger_output)

class UnhandledAppError(AppError):
    def __init__(self, descriptioon, logger_output=None):
        super().__init__("UnhandledAppError", description, logger_output)
