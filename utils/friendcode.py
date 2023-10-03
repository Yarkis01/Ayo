from utils.database import Collections, Database
import re


async def ensure_user_exists(database: Database, id: int) -> None:
    """Checks if a user with the given ID exists in the database.
    If the user does not exist, creates them with default information.

    Args:
        database (Database): Database instance
        id (int): ID of the user to check/create

    Returns:
        None
    """
    data = await database.find_one(Collections.FRIEND_CODE, {"uid": id})

    if not data:
        await database.insert_document(
            Collections.FRIEND_CODE,
            {
                "uid": id,
                "publicAccess": True,
                "friendCode": {
                    "ds": None,
                    "switch": None,
                    "cafemix": None,
                    "pogo": None,
                    "home": None,
                    "master": None,
                    "shuffle": None,
                    "sleep": None,
                    "unite": None,
                },
            },
        )


def format_key(code_type: str) -> str:
    """
    Format a code_type string into its corresponding game console or service name.

    Args:
        code_type (str): The code_type representing a specific game console or service.

    Returns:
        str: The formatted name of the game console or service, or the original code_type if not recognized.
    """
    match code_type:
        case "ds":
            return "Nintendo 3DS"
        case "switch":
            return "Nintendo Switch"
        case "cafemix":
            return "Pokémon Café Mix"
        case "pogo":
            return "Pokémon Go"
        case "home":
            return "Pokémon Home"
        case "master":
            return "Pokémon Master"
        case "shuffle":
            return "Pokémon Shuffle"
        case "sleep":
            return "Pokémon Sleep"
        case "unite":
            return "Pokémon UNITE"
        case _:
            return code_type


class CodeChecker:
    """
    A utility class to check and format codes for various game consoles and services.

    Attributes:
        CODE_LENGTHS (dict): A dictionary containing code_type as keys and their respective expected code lengths as values.
    """

    CODE_LENGTHS = {
        "ds": 12,
        "switch": 12,
        "cafemix": 12,
        "pogo": 12,
        "home": 12,
        "master": 16,
        "shuffle": 8,
        "sleep": 12,
        "unite": 7,
    }

    def __format_string(self, code_type: str, code: str) -> str:
        """
        Format the code string by removing unnecessary characters and modifying specific code_types.

        Args:
            code_type (str): The code_type representing a specific game console or service.
            code (str): The code to be formatted.

        Returns:
            str: The formatted code string.
        """
        code = code.lower().replace("-", "")
        if code_type == "switch":
            code = code.replace("sw", "")

        return code

    def check(self, code_type: str, code: str) -> bool:
        """
        Check the validity of a given code for a specific game console or service.

        Args:
            code_type (str): The code_type representing a specific game console or service.
            code (str): The code to be validated.

        Returns:
            bool: True if the code is valid for the given code_type, False otherwise.
        """
        if code_type not in self.CODE_LENGTHS:
            return False

        code = self.__format_string(code_type, code)

        if len(code) != self.CODE_LENGTHS[code_type]:
            return False

        if code_type in {"home", "shuffle"}:
            return code.isalpha()

        pattern = (
            r"^\d+(-\d+){0,2}$"
            if code_type not in {"cafemix", "unite"}
            else r"^\w+(-\w+){0,2}$"
        )
        return bool(re.match(pattern, code))

    def format(self, code_type: str, code: str) -> str:
        """
        Format a code string according to the specified game console or service.

        Args:
            code_type (str): The code_type representing a specific game console or service.
            code (str): The code to be formatted.

        Returns:
            str: The formatted code string.
        """
        code = self.__format_string(code_type, code)

        if self.CODE_LENGTHS[code_type] == 12 and code_type != "home":
            code = f"{code[:4]}-{code[4:8]}-{code[8:12]}"
            if code_type == "switch":
                code = f"SW-{code}"
        elif code_type == "master":
            code = f"{code[:4]}-{code[4:8]}-{code[8:12]}-{code[12:16]}"

        return code.upper()
