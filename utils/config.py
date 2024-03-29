from typing import List
from dotenv import load_dotenv
import ast
import os


class Config:
    """Configuration class to load environment variables."""

    def __init__(self):
        """Initialize the Config class.

        Loads the environment variables from the `.env` file
        using the `python-dotenv` module.
        """

        load_dotenv()

        self.__mongo_uri = os.getenv("MONGO_URI")
        self.__discord_token = os.getenv("DISCORD_TOKEN")
        self.__bot_version = os.getenv("BOT_VERSION")
        self.__support_server = os.getenv("SUPPORT_SERVER")

        self.__test_guilds = ast.literal_eval(os.getenv("TEST_GUILDS"))
        self.__dev_mode = ast.literal_eval(os.getenv("DEV_MODE"))
        self.__logs_channel = ast.literal_eval(os.getenv("LOGS_CHANNEL"))

        self.__enabled_modules = (
            os.getenv("ENABLED_MODULES").replace(" ", "").split(",")
        )
        self.__disabled_modules = (
            os.getenv("DISABLED_MODULES").replace(" ", "").split(",")
        )

        self.__splatoon2_api = os.getenv("SPLATOON2_API")
        self.__splatoon3_api = os.getenv("SPLATOON3_API")
        self.__timezone = os.getenv("TIMEZONE")

        self.__rotations_channel = os.getenv("ROTATIONS_CHANNEL")
        self.__rotations_role = os.getenv("ROTATIONS_ROLE")

        self.__data_retention = os.getenv("DATA_RETENTION")

    @property
    def mongo_uri(self) -> str:
        """Get the MongoDB URI value.

        Returns:
            str: The MongoDB URI read from the `.env` file.
        """

        return self.__mongo_uri

    @property
    def discord_token(self) -> str:
        """Get the Discord token value.

        Returns:
            str: The Discord token read from the `.env` file.
        """

        return self.__discord_token

    @property
    def bot_version(self) -> str:
        """Get the bot version string.

        Returns:
            str: The bot version read from the `.env` file.
        """

        return self.__bot_version

    @property
    def support_server(self) -> str:
        """Get support server link.

        Returns:
            str: Support server link read from `.env` file.
        """

        return self.__support_server

    @property
    def test_guilds(self) -> tuple:
        """Get the number of test guilds.

        Returns:
            tuple: The number of guilds to use for testing.
        """

        return (
            self.__test_guilds
            if isinstance(self.__test_guilds, tuple)
            else (self.__test_guilds,)
        )

    @property
    def dev_mode(self) -> bool:
        """Get the dev mode boolean status.

        Returns:
            bool: True if dev mode is enabled, False otherwise.
        """

        return self.__dev_mode

    @property
    def logs_channel(self) -> int:
        """Get logging channel ID

        Returns:
            int: Logging channel ID
        """

        return self.__logs_channel

    @property
    def enabled_modules(self) -> List[str]:
        """Get the list of enabled module names.

        Returns:
            List[str]: The list of enabled module names.
        """

        return self.__enabled_modules

    @property
    def disabled_modules(self) -> List[str]:
        """Get the list of disabled module names.

        Returns:
            List[str]: The list of disabled module names.
        """

        return self.__disabled_modules

    @property
    def splatoon2_api(self) -> str:
        """Get the Splatoon 2 API URL.

        Returns:
            str: The Splatoon 2 API URL read from the `.env` file.
        """

        return self.__splatoon2_api

    @property
    def splatoon3_api(self) -> str:
        """Get the Splatoon 3 API URL.

        Returns:
            str: The Splatoon 3 API URL read from the `.env` file.
        """

        return self.__splatoon3_api

    @property
    def timezone(self) -> str:
        """Get the timezone.

        Returns:
            str: The timezone read from the `.env` file.
        """

        return self.__timezone

    @property
    def rotations_channel(self) -> int:
        """Get the rotation channel ID.

        Returns:
            int: The rotation channel ID read from the `.env` file.
        """
        return self.__rotations_channel

    @property
    def rotations_role(self) -> int:
        """Get the rotation role ID.

        Returns:
            int: The rotation role ID read from the `.env` file.
        """
        return self.__rotations_role

    @property
    def data_retention(self) -> int:
        """Get the data retention time in seconds.

        Returns:
            int: The data retention time in seconds read from the `.env` file.
        """
        return int(self.__data_retention)
