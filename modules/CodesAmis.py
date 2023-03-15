import disnake, config, qrcode, os, asyncio
from disnake.ext import commands, tasks

from helper.codesamis import Database
from utils.logger import logs

CHOICES = {
    "Nintendo 3DS (XXXX-XXXX-XXXX)": "ds",
    "Nintendo Switch (SW-XXXX-XXXX-XXXX)": "switch",
    "Pokémon Home (XXXXXXXXXXXX)": "home",
    "Pokémon GO (XXXX-XXXX-XXXX)": "pogo",
    "Pokémon Master (XXXX-XXXX-XXXX-XXXX)": "master",
    "Pokémon Shuffle (XXXXXXXX)": "shuffle",
    "Pokémon Cafemix (XXXX-XXXX-XXXX)": "cafemix"
}
QRCODE_CHOICES = {
    "Pokémon Home": "home",
    "Pokémon GO": "pogo"
}
QRCODES_TYPE = {
    "home": "Pokémon Home",
    "pogo": "Pokémon GO"
}
TYPES = ["ds", "switch", "home", "pogo", "master", "shuffle", "cafemix"]

class CodesAmisModule(commands.Cog):
    def __init__(self, bot: commands.AutoShardedInteractionBot):
        self.__bot = bot
        self.__db  = None

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        if not self.__db:
            self.__db = Database("databases/CodesAmis.db")
            await self.__db.create_if_not_exists()
            await self.__db.is_user_exists(52)
        logs.success("Le module a été initié correctement", "[CODES-AMIS]")


def setup(self) -> None:
    if config.CODESAMIS_ENABLED:
        self.add_cog(CodesAmisModule(self))
        logs.info("Le module a bien été détécté et chargé", "[CODES-AMIS]")
    else:
        logs.warning("Le module n'a pas été chargé car il est désactivé dans la configuration", "[CODES-AMIS]")