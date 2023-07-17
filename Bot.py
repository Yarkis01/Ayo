import sys ; sys.dont_write_bytecode = True
from pathlib import Path
import time

from disnake.ext import commands
import disnake

from utils.config      import Config
from utils.database    import Database, Collections
from utils.embed       import Embed
from utils.logger      import Logger, DiscordLogger

class AyoBot(commands.AutoShardedInteractionBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    async def on_ready(self) -> None:
        # Initiates the Discord logging system
        await self.logger.check_channel(self)
        
        # Initialize collections in the database if it doesn't already exist
        for collection in Collections:
            await self.database.init_collection(collection)

        # Set the bot's presence
        await self.change_presence(
            activity = disnake.Activity(
                name = f"Splatoon 3 | {self.config.bot_version}",
                type = disnake.ActivityType.playing,
            ),
            status = disnake.Status.do_not_disturb
        )
        
        # Sends a message to say that the bot is online and operational 
        await self.logger.send(embed = Embed.default(
            title       = ":robot: Bot paré au combat !",
            description = "Prêt à liquider DJ Octave."
        ))
        Logger.success(f"Successful login as {self.user}")
        
    async def on_guild_join(self, guild: disnake.Guild) -> None:
        bot_invite = ""

        for channel in await guild.fetch_channels():
            if channel.type == disnake.ChannelType.text and channel.permissions_for(guild.me).create_instant_invite:
                if "COMMUNITY" in guild.features:
                    bot_invite = await channel.create_invite(max_age = 0)
                else:
                    bot_invite = await channel.create_invite(max_age = 2592000)

                break
        
        await self.database.insert_document(Collections.GUILDS, {
            "guildId"   : guild.id,
            "language"  : "fr",
            "invitation": f"https://discord.gg/{bot_invite.code}",
            "joinTime"  : int(time.time())
        })
        
        await self.logger.send(embed = Embed.default(
            title       = "📈 Le bot a rejoint un nouveaux serveur !",
            description = f"Le bot est à présent sur **{len(self.guilds)} serveurs**."
        ))

    async def on_guild_remove(self, guild: disnake.Guild) -> None:
        for collection in Collections:
            await self.database.delete_document(collection, {"guildId": guild.id})
            
        await self.logger.send(embed = Embed.default(
            title       = "📉 Le bot a été retiré d'un serveur !",
            description = f"Le bot est à présent sur **{len(self.guilds)} serveurs**."
        ))


if __name__ == '__main__':
    config = Config()
    
    # Create an instance of the AyoBot
    bot = AyoBot(
        intents     = disnake.Intents.default(),
        test_guilds = [config.test_guilds] if config.dev_mode else None
    )
    
    # Set additional properties for the bot
    bot.config   = config
    bot.database = Database(config.mongo_uri)
    bot.logger   = DiscordLogger(config.logs_channel)

    # Define the folders for modules
    modules_folder = Path("./modules/")
    enabled_folder = config.enabled_modules
    
    loaded_modules = []
    
    # Load modules
    for path in modules_folder.glob("*.py"):
        name = path.stem
        
        if name not in enabled_folder:
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