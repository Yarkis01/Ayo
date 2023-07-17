from typing import List
from dotenv import load_dotenv
import os

class Config:
    """Configuration class to load environment variables."""

    def __init__(self):
        """Initialize the Config class.
        
        Loads the environment variables from the `.env` file
        using the `python-dotenv` module.
        """
        
        load_dotenv()

        self.__mongo_uri     = os.getenv("MONGO_URI")
        self.__discord_token = os.getenv("DISCORD_TOKEN")
        self.__bot_version   = os.getenv("BOT_VERSION")

        self.__test_guilds   = int(os.getenv("TEST_GUILDS"))
        self.__dev_mode      = bool(os.getenv("DEV_MODE"))
        self.__logs_channel  = int(os.getenv("LOGS_CHANNEL"))

        self.__enabled_modules  = os.getenv("ENABLED_MODULES").split(",") 
        self.__disabled_modules = os.getenv("DISABLED_MODULES").split(",")

    @property
    def discord_token(self) -> str:
        """Get the Discord token value.

        Returns:
            str: The Discord token read from the `.env` file.
        """

        return self.__discord_token

    @property
    def mongo_uri(self) -> str:
        """Get the MongoDB URI value.

        Returns:
            str: The MongoDB URI read from the `.env` file.
        """

        return self.__mongo_uri
    
    @property
    def test_guilds(self) -> int:
        """Get the number of test guilds.

        Returns:
            int: The number of guilds to use for testing.
        """
        
        return self.__test_guilds

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
    def bot_version(self) -> str:
        """Get the bot version string.

        Returns:
            str: The bot version read from the `.env` file.
        """

        return self.__bot_version

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