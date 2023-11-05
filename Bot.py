import sys

sys.dont_write_bytecode = True

from datetime import datetime, timedelta
from pathlib import Path
import time
import traceback

from disnake.ext import commands, tasks
import disnake
import pytz

from utils.config import Config
from utils.database import Database, Collections
from utils.embed import Embed
from utils.error import error_message_generator, excepthook
from utils.logger import Logger, DiscordLogger
from utils.requests import update_data_if_needed


class InviteView(disnake.ui.View):
    def __init__(self, code: str):
        super().__init__()
        self.add_item(
            disnake.ui.Button(
                label="Rejoindre le serveur", url=f"https://discord.gg/{code}"
            )
        )


class AyoBot(commands.AutoShardedInteractionBot):
    def __init__(self, *args, **kwargs):
        self.__update_data_started = False
        super().__init__(*args, **kwargs)

    @tasks.loop(seconds=5)
    async def _update_data_loop(self) -> None:
        now = self.__timezone.localize(datetime.utcnow())

        if (self.__next_update_data - now) >= timedelta(hours=0):
            return

        await update_data_if_needed(
            f"{self.config.splatoon3_api}/locale/fr-FR.json",
            "./data/s3/translation.json",
        )
        await update_data_if_needed(
            f"{self.config.splatoon2_api}/locale/fr.json", "./data/s2/translation.json"
        )

        self.__next_update_data = self.__timezone.localize(
            datetime(now.year, now.month, now.day, now.hour, 0, 0, 0)
            + timedelta(hours=2 if now.hour % 2 == 0 else 1)
        )

    @tasks.loop(hours=12)
    async def _delete_inactive_guilds_loop(self) -> None:
        for guild in await self.database.find_documents(Collections.GUILDS, {}):
            if guild["lastMessageTime"] + self.config.data_retention < int(time.time()):
                await self.database.delete_document(
                    Collections.GUILDS, {"guildId": guild["guildId"]}
                )

    @tasks.loop(hours=12)
    async def _delete_inactive_users_loop(self) -> None:
        for user in await self.database.find_documents(Collections.USERS, {}):
            if user["lastMessageTime"] + self.config.data_retention < int(time.time()):
                for collection in Collections:
                    await self.database.delete_document(
                        collection, {"uid": user["uid"]}
                    )

    async def add_guild(self, guild: disnake.Guild, bot_invite: str = "") -> None:
        await self.database.insert_document(
            Collections.GUILDS,
            {
                "guildId": guild.id,
                "language": "fr",
                "invitation": f"https://discord.gg/{bot_invite}",
                "joinTime": int(time.time()),
                "lastMessageTime": int(time.time()),
            },
        )

    async def on_connect(self) -> None:
        if not self.__update_data_started:
            self.__update_data_started = True
            self.__timezone = pytz.timezone(self.config.timezone)
            self.__next_update_data = self.__timezone.localize(
                datetime(1970, 1, 1, 0, 0, 0, 0)
            )
            self._update_data_loop.start()
            self._delete_inactive_guilds_loop.start()
            self._delete_inactive_users_loop.start()

    async def on_ready(self) -> None:
        # Initiates the Discord logging system
        await self.logger.check_channel(self)

        # Initialize collections in the database if it doesn't already exist
        for collection in Collections:
            await self.database.init_collection(collection)

        # Set the bot's presence
        await self.change_presence(
            activity=disnake.Activity(
                name=f"Splatoon 3 | {self.config.bot_version}",
                type=disnake.ActivityType.playing,
            ),
            # status = disnake.Status.do_not_disturb
            status=disnake.Status.online,
        )

        # Sends a message to say that the bot is online and operational
        await self.logger.send(
            embed=Embed.default(
                title=":robot: Bot paré au combat !",
                description="Prêt à liquider DJ Octave.",
            )
        )
        Logger.success(f"Successful login as {self.user}")

    async def on_guild_join(self, guild: disnake.Guild) -> None:
        bot_invite = ""

        for channel in await guild.fetch_channels():
            if (
                channel.type == disnake.ChannelType.text
                and channel.permissions_for(guild.me).create_instant_invite
            ):
                if "COMMUNITY" in guild.features:
                    bot_invite = await channel.create_invite(max_age=0)
                else:
                    bot_invite = await channel.create_invite(max_age=2592000)
                bot_invite = bot_invite.code
                break

        await self.add_guild(guild, bot_invite)

        await self.logger.send(
            embed=Embed.default(
                title="📈 Le bot a rejoint un nouveaux serveur !",
                description=f"Le bot est à présent sur **{len(self.guilds)} serveurs**.",
            ),
            view=InviteView(bot_invite) if bot_invite else disnake.utils.MISSING,
        )

    async def on_guild_remove(self, guild: disnake.Guild) -> None:
        for collection in Collections:
            await self.database.delete_document(collection, {"guildId": guild.id})

        await self.logger.send(
            embed=Embed.default(
                title="📉 Le bot a été retiré d'un serveur !",
                description=f"Le bot est à présent sur **{len(self.guilds)} serveurs**.",
            )
        )

    async def on_slash_command(self, inter: disnake.CommandInteraction) -> None:
        """
        Handles the execution of a slash command interaction.

        This function is called when a slash command interaction occurs. It updates the last message time for the guild and the user associated with the interaction in the database.

        Args:
            inter (disnake.CommandInteraction): The slash command interaction object.

        Returns:
            None
        """
        if not inter.guild.id:
            return

        # Update lastMessageTime (used to delete inactive guilds)
        if not await self.database.find_one(
            Collections.GUILDS, {"guildId": inter.guild.id}
        ):
            await self.add_guild(inter.guild)
            return

        await self.database.update_document(
            Collections.GUILDS,
            {"guildId": inter.guild.id},
            {"lastMessageTime": int(time.time())},
        )

        # Update lastMessageTime (used to delete inactive users)
        if not await self.database.find_one(
            Collections.USERS, {"uid": inter.author.id}
        ):
            await self.database.insert_document(
                Collections.USERS,
                {
                    "uid": inter.author.id,
                    "lastMessageTime": int(time.time()),
                },
            )
            return

        await self.database.update_document(
            Collections.USERS,
            {"uid": inter.author.id},
            {"lastMessageTime": int(time.time())},
        )

    async def on_slash_command_error(
        self,
        inter: disnake.ApplicationCommandInteraction,
        exception: commands.CommandError,
    ) -> None:
        await error_message_generator(bot, inter, exception)

    async def on_user_command_error(
        self,
        inter: disnake.ApplicationCommandInteraction,
        exception: commands.CommandError,
    ) -> None:
        await error_message_generator(bot, inter, exception)

    async def on_error(self, *args, **kwargs) -> None:
        Logger.fail("An error has occurred", "error")
        Logger.log_to_file(
            f"Args: {args}\nKwargs: {kwargs}\nTraceback: {traceback.format_exc()}"
        )

        await self.logger.send(
            embed=Embed.error(
                title=":x: Une erreur est survenue",
                description=f"Args: ```{args}```\nKwargs: ```{kwargs}```\nErreur: ```{traceback.format_exc()}```",
            )
        )


if __name__ == "__main__":
    sys.excepthook = excepthook

    config = Config()

    test_guilds = None
    if config.dev_mode:
        test_guilds = config.test_guilds
        Logger.dev(f"Test servers: {test_guilds}")

    # Create an instance of the AyoBot
    bot = AyoBot(intents=disnake.Intents.default(), test_guilds=test_guilds)

    # Set additional properties for the bot
    bot.config = config
    bot.database = Database(config.mongo_uri)
    bot.logger = DiscordLogger(config.logs_channel)

    loaded_modules = []

    # Load modules
    for path in Path("./modules/").glob("*.py"):
        name = path.stem

        if name not in config.enabled_modules:
            Logger.warning(f"{name} is disabled, skipping...", "modules")
            continue

        try:
            bot.load_extension(f"modules.{name}")
            loaded_modules.append(name)
            Logger.info(f"{name} loaded successfully", "modules")
        except Exception as e:
            Logger.fail(f"Error loading {name}: {e}", "modules")

    if not loaded_modules:
        Logger.warning("No modules loaded!", "modules")

    # Run bot
    bot.run(config.discord_token)
