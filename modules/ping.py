from datetime import datetime
import asyncio
import math
import sys

from disnake.ext import commands, tasks
import disnake
import humanize

from utils.config   import Config
from utils.embed    import Embed
from utils.logger   import Logger
from utils.requests import make_api_request

import math

SIZE_UNITS = ["octets", "Ko", "Mo", "Go", "To", "Po", "Eo", "Zo", "Yo"]

def convert_size(size_bytes):
    if size_bytes == 0:
        return "0 octet"
    
    i = min(int(math.log(size_bytes, 1024)), len(SIZE_UNITS) - 1)
    size = size_bytes / (1024 ** i)

    return f"{size:.2f} {SIZE_UNITS[i]}"

class PingModule(commands.Cog):
    def __init__(self, bot: commands.AutoShardedInteractionBot):
        self.__bot            = bot
        self.__config: Config = bot.config
        
        self.__is_started  = False
        self.__start_time  = datetime.now()
        self.__uptime_data = None
        self.__usage_data  = None
        
        humanize.activate("fr_FR")

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        if not self.__is_started:
            await asyncio.gather(
                self._is_alive_loop.start(),
                self._update_loop.start()
            )
            self.__is_started = True

    @tasks.loop(seconds = 60)
    async def _is_alive_loop(self) -> None:
        response = await make_api_request(self.__config.uptimekuma_url)
        if not response:
            Logger.warning("Monitor not found or not active", "ping")

    @tasks.loop(minutes = 30)
    async def _update_loop(self) -> None:
        self.__uptime_data = await make_api_request(self.__config.watchbot_api, headers = {"AUTH-TOKEN": self.__config.watchbot_key})
        if not self.__uptime_data:
            Logger.warning("Unable to contact Watchbot API", "ping")

        usage_data = await make_api_request(self.__config.pterodactyl_api, headers = {"Authorization": f"Bearer {self.__config.pterodactyl_key}"})
        if usage_data:
            self.__usage_data = usage_data['attributes']['resources']
        else:
            Logger.warning("Unable to contact the Pterodactyl API", "ping")

    @commands.slash_command(name = "ping", description = "Permet d'obtenir plein d'information (in)utile sur le bot", dm_permission = False)
    async def _ping_command(self, inter: disnake.CommandInteraction) -> None:
        await inter.response.defer(ephemeral = True)
        
        embed = Embed.default(
            title       = "📊 Statistiques (in)utile",
            description = "Voici plein d'information fortement (in)utile sur le bot."
        ).add_field(
            name  = "🏓 Latence du bot",
            value = f"{int(self.__bot.latency * 1000)}ms"
        ).add_field(
            name  = f"<:shard:1038454850846990337> Latence (Shard #{inter.guild.shard_id})",
            value = f"{int(self.__bot.latencies[inter.guild.shard_id][1] * 1000)}ms"
        ).add_field(
            name   = "🕛 Temps en ligne",
            value  = f"{humanize.precisedelta(datetime.now() - self.__start_time)}"
        )
        
        if self.__uptime_data:
            for data in ["7d", "30d", "90d"]:
                try:
                    uptime = float(self.__uptime_data[data])
                
                    if uptime < 75.0:
                        name = f"<:red_clock:1038773522106941530> Uptime ({data.replace('d', '')} jours)"
                    elif uptime < 98.0:
                        name = f"<:orange_clock:1038775657406140467> Uptime ({data.replace('d', '')} jours)"
                    else:
                        name = f"<:green_clock:1038775694655758386> Uptime ({data.replace('d', '')} jours)"
                except TypeError:
                    name   = f"<:unknown_clock:1055937372828741712> Uptime ({data.replace('d', '')} jours)"
                    uptime = "???"
                    
                embed.add_field(
                    name   = name,
                    value  = f"{uptime} %"
                )

        if self.__usage_data:
            embed.add_field(
                name   = "<:cpu:1038771595164012545> CPU",
                value  = f"{self.__usage_data['cpu_absolute']} %",
                inline = True
            ).add_field(
                name   = "<:ram:1038771604622168194> Mémoire Vive",
                value  = convert_size(self.__usage_data['memory_bytes']),
                inline = True
            ).add_field(
                name   = "<:hdd:1038771601468043385> Espace Disque",
                value  = convert_size(self.__usage_data['disk_bytes']),
                inline = True
            )
        
        embed.add_field(
            name   = "<:python:1088566268552028190> Python",
            value  = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        ).add_field(
            name   = "<:disnake:1088566257135140984> Disnake",
            value  = f"{disnake.version_info.major}.{disnake.version_info.minor}.{disnake.version_info.micro}"
        ).add_field(
            name   = "🤖 Version",
            value  = self.__config.bot_version
        )
        
        await inter.send(embed = embed.set_footer(text = "Données actualisées toutes les 30 minutes"))

def setup(self) -> None:
    self.add_cog(PingModule(self))
    Logger.success("The module has been started correctly", "ping")