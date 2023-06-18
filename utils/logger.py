import datetime

class bcolors:
    INFO    = '\033[96m'
    SUCCESS = '\033[92m'
    WARNING = '\033[93m'
    FAIL    = '\033[91m'
    ENDC    = '\033[0m'

class logs:
    @staticmethod
    def print_log(message: str, log_type: str, log_custom: str = "") -> None:
        """
        Print a log message with the specified log type and message.

        Args:
            message (str): The log message.
            log_type (str): The log type (e.g., INFO, SUCCESS, WARNING, FAIL).
            log_custom (str): Optional type of the log message.
        """
        timestamp = datetime.datetime.now().strftime('%H:%M:%S')
        log_color = getattr(bcolors, log_type.upper(), "")

        if log_custom:
            print(f"{log_color}[{timestamp}][{log_type.upper()}][{log_custom.upper()}]: {message}{bcolors.ENDC}")
        else:
            print(f"{log_color}[{timestamp}][{log_type.upper()}]: {message}{bcolors.ENDC}")

    @staticmethod
    def warning(message: str, log_custom: str = "") -> None:
        """
        Print a warning log message.

        Args:
            message (str): The log message.
            log_custom (str): Optional type of the log message.
        """
        logs.print_log(message, "WARNING", log_custom)

    @staticmethod
    def success(message: str, log_custom: str = "") -> None:
        """
        Print a success log message.

        Args:
            message (str): The log message.
            log_custom (str): Optional type of the log message.
        """
        logs.print_log(message, "SUCCESS", log_custom)

    @staticmethod
    def fail(message: str, log_custom: str = "") -> None:
        """
        Print a fail log message.

        Args:
            message (str): The log message.
            log_custom (str): Optional type of the log message.
        """
        logs.print_log(message, "FAIL", log_custom)

    @staticmethod
    def info(message: str, log_custom: str = "") -> None:
        """
        Print an info log message.

        Args:
            message (str): The log message.
            log_custom (str): Optional type of the log message.
        """
        logs.print_log(message, "INFO", log_custom)
