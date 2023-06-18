import datetime

class bcolors:
    INFO    = '\033[96m'
    SUCCESS = '\033[92m'
    WARNING = '\033[93m'
    FAIL    = '\033[91m'
    ENDC    = '\033[0m'

class logs:
    @staticmethod
    def print_log(message: str, log_type: str) -> None:
        """
        Print a log message with the specified log type and message.

        Args:
            message (str): The log message.
            log_type (str): The log type (e.g., INFO, SUCCESS, WARNING, FAIL).
        """
        timestamp = datetime.datetime.now().strftime('%H:%M:%S')
        log_color = getattr(bcolors, log_type.upper(), "")

        print(f"{log_color}[{timestamp}][{log_type.upper()}]: {message}{bcolors.ENDC}")

    @staticmethod
    def warning(message: str, log_type: str = "") -> None:
        """
        Print a warning log message.

        Args:
            message (str): The log message.
            log_type (str): Optional type of the log message.
        """
        logs.print_log(message, "WARNING")

    @staticmethod
    def success(message: str, log_type: str = "") -> None:
        """
        Print a success log message.

        Args:
            message (str): The log message.
            log_type (str): Optional type of the log message.
        """
        logs.print_log(message, "SUCCESS")

    @staticmethod
    def fail(message: str, log_type: str = "") -> None:
        """
        Print a fail log message.

        Args:
            message (str): The log message.
            log_type (str): Optional type of the log message.
        """
        logs.print_log(message, "FAIL")

    @staticmethod
    def info(message: str, log_type: str = "") -> None:
        """
        Print an info log message.

        Args:
            message (str): The log message.
            log_type (str): Optional type of the log message.
        """
        logs.print_log(message, "INFO")
