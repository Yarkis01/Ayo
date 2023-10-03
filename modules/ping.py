from datetime import datetime
import math
import sys
import psutil

from disnake.ext import commands, tasks
import disnake
import humanize

from utils.config import Config
from utils.embed import Embed
from utils.logger import Logger
from utils.requests import make_api_request

import math

SIZE_UNITS = ["octets", "Ko", "Mo", "Go", "To", "Po", "Eo", "Zo", "Yo"]


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0 octet"

    i = min(int(math.log(size_bytes, 1024)), len(SIZE_UNITS) - 1)
    size = size_bytes / (1024**i)

    return f"{size:.2f} {SIZE_UNITS[i]}"


class PingModule(commands.Cog):
    def __init__(self, bot: commands.AutoShardedInteractionBot):
        self.__bot = bot
        self.__config: Config = bot.config

        self.__start_time = datetime.now()
        self.__process = psutil.Process()

        humanize.activate("fr_FR")

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        Logger.success("The module has been started correctly", "ping")

    @commands.slash_command(
        name="ping",
        description="Permet d'obtenir plein d'information (in)utile sur le bot",
        dm_permission=False,
    )
    async def _ping_command(self, inter: disnake.CommandInteraction) -> None:
        await inter.response.defer(ephemeral=True)

        embed = (
            Embed.default(
                title="📊 Statistiques (in)utile",
                description="Voici plein d'information fortement (in)utile sur le bot.",
            )
            .add_field(
                name="🏓 Latence du bot", value=f"{int(self.__bot.latency * 1000)}ms"
            )
            .add_field(
                name=f"<:shard:1038454850846990337> Latence (Shard #{inter.guild.shard_id})",
                value=f"{int(self.__bot.latencies[inter.guild.shard_id][1] * 1000)}ms",
            )
            .add_field(
                name="🕛 Temps en ligne",
                value=f"{humanize.precisedelta(datetime.now() - self.__start_time)}",
            )
        )

        embed.add_field(
            name="<:cpu:1038771595164012545> CPU",
            value=f"{self.__process.cpu_percent()} %",
            inline=True,
        ).add_field(
            name="<:ram:1038771604622168194> Mémoire Vive",
            value=convert_size(self.__process.memory_info().rss),
            inline=True,
        ).add_field(
            name="<:hdd:1038771601468043385> Espace Disque",
            # value  = convert_size(psutil.disk_usage(sys.path[0])[1]),r
            value="???",
            inline=True,
        ).add_field(
            name="<:python:1088566268552028190> Python",
            value=f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        ).add_field(
            name="<:disnake:1088566257135140984> Disnake",
            value=f"{disnake.version_info.major}.{disnake.version_info.minor}.{disnake.version_info.micro}",
        ).add_field(
            name="🤖 Version", value=self.__config.bot_version
        )

        await inter.send(embed=embed)


def setup(self) -> None:
    self.add_cog(PingModule(self))
