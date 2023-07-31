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

        self.__mongo_uri      = os.getenv("MONGO_URI")
        self.__discord_token  = os.getenv("DISCORD_TOKEN")
        self.__bot_version    = os.getenv("BOT_VERSION")
        self.__support_server = os.getenv("SUPPORT_SERVER")

        self.__test_guilds   = ast.literal_eval(os.getenv("TEST_GUILDS"))
        self.__dev_mode      = ast.literal_eval(os.getenv("DEV_MODE"))
        self.__logs_channel  = ast.literal_eval(os.getenv("LOGS_CHANNEL"))

        self.__enabled_modules  = os.getenv("ENABLED_MODULES").replace(" ", "").split(",") 
        self.__disabled_modules = os.getenv("DISABLED_MODULES").replace(" ", "").split(",")
        
        self.__pterodactyl_api = os.getenv("PTERODACTYL_API")
        self.__pterodactyl_key = os.getenv("PTERODACTYL_KEY")
        
        self.__watchbot_api = os.getenv("WATCHBOT_URL")
        self.__watchbot_key = os.getenv("WATCHBOT_KEY")
        
        self.__uptimekuma_url = os.getenv("UPTIMEKUMA_URL")
        
        self.__splatoon2_api = os.getenv("SPLATOON2_API")
        self.__splatoon3_api = os.getenv("SPLATOON3_API")
        self.__timezone      = os.getenv("TIMEZONE")

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
        
        return self.__test_guilds if isinstance(self.__test_guilds, tuple) else (self.__test_guilds,)

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
    def pterodactyl_api(self) -> str:
        """Get the Pterodactyl API URL.
        
        Returns:
            str: The Pterodactyl API URL read from the `.env` file.
        """
        
        return self.__pterodactyl_api

    @property
    def pterodactyl_key(self) -> str:
        """Get the Pterodactyl API key.
        
        Returns:
            str: The Pterodactyl API key read from the `.env` file. 
        """
        
        return self.__pterodactyl_key

    @property
    def watchbot_api(self) -> str:
        """Get the Watchbot API URL.
        
        Returns:
            str: The Watchbot API URL read from the `.env` file.
        """
        
        return self.__watchbot_api

    @property 
    def watchbot_key(self) -> str:
        """Get the Watchbot API key.
        
        Returns:
            str: The Watchbot API key read from the `.env` file.
        """
        
        return self.__watchbot_key

    @property
    def uptimekuma_url(self) -> str:
        """Get the Uptime Kuma status page URL.
        
        Returns:
            str: The Uptime Kuma status page URL read from the `.env` file.
        """
        
        return self.__uptimekuma_url
    
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