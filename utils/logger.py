from typing import List
from datetime import datetime
from disnake.ext import commands
import disnake
import contextlib

FILENAME = f"logs_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"


class LogColors:
    INFO = "\033[96m"
    SUCCESS = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    DEV = "\033[95m"
    ENDC = "\033[0m"


class Logger:
    @staticmethod
    def log_to_file(message: str) -> None:
        """
        Log a message to the file.

        Args:
            message (str): The log message.
        """
        with open(f"./logs/{FILENAME}", "a") as logs_file:
            logs_file.write(message)

    @staticmethod
    def print_log(message: str, log_type: str, log_custom: str = "") -> None:
        """
        Print a log message with the specified log type and message.

        Args:
            message (str): The log message.
            log_type (str): The log type (e.g., INFO, SUCCESS, WARNING, FAIL).
            log_custom (str): Optional type of the log message.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_color = getattr(LogColors, log_type.upper(), "")

        Logger.log_to_file(
            f"[{timestamp}][{log_type.upper()}]{f'[{log_custom.upper()}]' if log_custom else ''}: {message}\n"
        )

        if log_custom:
            print(
                f"{log_color}[{timestamp}][{log_type.upper()}][{log_custom.upper()}]: {message}{LogColors.ENDC}"
            )
        else:
            print(
                f"{log_color}[{timestamp}][{log_type.upper()}]: {message}{LogColors.ENDC}"
            )

    @staticmethod
    def warning(message: str, log_custom: str = "") -> None:
        """
        Print a warning log message.

        Args:
            message (str): The log message.
            log_custom (str): Optional type of the log message.
        """
        Logger.print_log(message, "WARNING", log_custom)

    @staticmethod
    def success(message: str, log_custom: str = "") -> None:
        """
        Print a success log message.

        Args:
            message (str): The log message.
            log_custom (str): Optional type of the log message.
        """
        Logger.print_log(message, "SUCCESS", log_custom)

    @staticmethod
    def fail(message: str, log_custom: str = "") -> None:
        """
        Print a fail log message.

        Args:
            message (str): The log message.
            log_custom (str): Optional type of the log message.
        """
        Logger.print_log(message, "FAIL", log_custom)

    @staticmethod
    def info(message: str, log_custom: str = "") -> None:
        """
        Print an info log message.

        Args:
            message (str): The log message.
            log_custom (str): Optional type of the log message.
        """
        Logger.print_log(message, "INFO", log_custom)

    @staticmethod
    def dev(message: str, log_custom: str = "") -> None:
        """
        Print an dev log message.

        Args:
            message (str): The log message.
            log_custom (str): Optional type of the log message.
        """
        Logger.print_log(message, "DEV", log_custom)


class DiscordLogger:
    """
    Logger class for logging to Discord channel.
    """

    def __init__(self, logs_channel_id: int):
        """
        Initialize the logger with channel ID.

        Args:
            logs_channel_id (int): The ID of the logs channel.
        """
        self.__logs_channel_id = logs_channel_id
        self.__logs_channel = None

    async def check_channel(self, bot: commands.AutoShardedInteractionBot) -> None:
        """
        Check if the logs channel exists.

        Args:
            bot (commands.AutoShardedInteractionBot): The discord bot.

        Returns:
            bool: True if channel exists, False otherwise.
        """
        try:
            self.__logs_channel = await bot.fetch_channel(self.__logs_channel_id)
        except disnake.NotFound:
            self.__logs_channel = None

    async def send(
        self,
        content: str = None,
        embed: disnake.Embed = None,
        embeds: List[disnake.Embed] = None,
        view: disnake.ui.View = None,
    ) -> None:
        """
        Send a message to the logs channel.

        Args:
            content (str, optional): The content of the message.
            embed (disnake.Embed, optional): The embed to send.
            embeds (List[disnake.Embed], optional): List of embeds to send.
            view (disnake.ui.View, optional): A disnake view, for displaying elements such as buttons
        """
        with contextlib.suppress():
            if self.__logs_channel:
                await self.__logs_channel.send(
                    content=content, embed=embed, embeds=embeds, view=view
                )
