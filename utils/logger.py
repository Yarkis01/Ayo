import datetime

class bcolors:
    INFO    = '\033[96m'
    SUCCESS = '\033[92m'
    WARNING = '\033[93m'
    FAIL    = '\033[91m'
    ENDC    = '\033[0m'

class logs:
    def warning(message: str, _type: str = "") -> None:
        print(f"{bcolors.WARNING}[{datetime.datetime.now().strftime('%H:%M:%S')}][WARNING]{_type}: {message}{bcolors.ENDC}")

    def success(message: str, _type: str = "") -> None:
        print(f"{bcolors.SUCCESS}[{datetime.datetime.now().strftime('%H:%M:%S')}][SUCCESS]{_type}: {message}{bcolors.ENDC}")

    def fail(message: str, _type: str = "") -> None:
        print(f"{bcolors.FAIL}[{datetime.datetime.now().strftime('%H:%M:%S')}][FAIL]{_type}: {message}{bcolors.ENDC}")

    def info(message: str, _type: str = "") -> None:
        print(f"{bcolors.INFO}[{datetime.datetime.now().strftime('%H:%M:%S')}][INFO]{_type}: {message}{bcolors.ENDC}")