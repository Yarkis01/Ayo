from disnake.ext import commands
import disnake

from utils.database import Database, Collections
from utils.embed import Embed
from utils.logger import Logger

class LotteryModule(commands.Cog):
    def __init__(self, bot: commands.AutoShardedInteractionBot):
        self.__bot          = bot
        self.__db: Database = bot.database
    
    @commands.Cog.listener()
    async def on_ready(self) -> None:
        Logger.success("The module has been started correctly", "lottery")
        
    @commands.slash_command(name = "loterie", dm_permission = False)
    async def _lottery_command(self, inter: disnake.CommandInteraction) -> None:
        await inter.response.defer()
    
    @_lottery_command.sub_command(name = "capsulomate", description = "Obtiens les probabilités du Capsulomate")
    async def _shellout_command(self, inter: disnake.CommandInteraction) -> None:
        await inter.send(file = disnake.File("./data/s3/lottery/capsulomate.png"))
        
    @_lottery_command.sub_command(name = "boîte-mystère", description = "Obtiens les probabilités des boîtes mystères")
    async def _mystery_box(self, inter: disnake.CommandInteraction, catalog: str = commands.Param(name = "catalogue", choices = {"Initial": "catalogue", "Bonus": "catalogue_bonus"})) -> None:
        await inter.send(file = disnake.File(f"./data/s3/lottery/boite-mystere_{catalog}.png"))
        
    @_lottery_command.sub_command(name = "saison", description = "Obtiens les titres et les bannières rares de chaque saison")
    async def _season_command(self, inter: disnake.CommandInteraction, season: str = commands.Param(name = "saison")) -> None:
        data = await self.__db.find_one(Collections.SEASON, {"name": season})

        if not data: 
            await inter.send(embed = Embed.error(":x: Saison invalide", "Merci de bien vouloir préciser une saison valide."))
            return
    
        endDate = f"<t:{data['date']['end']}:d>" if data["date"]["end"] else "*Pas encore terminée*"
        
        await inter.send(embed = Embed.default(
            title = f"<:catalogue:1134140975397224481> {data['name']}",
            description = f"**Début de saison**: <t:{data['date']['start']}:d>\n**Fin de saison**: {endDate}"
        ).add_field(
            name  = "<:titre:1096453724219641931> Titre",
            value = f"- {data['reward']['title']['adjective']}\n- {data['reward']['title']['subject']}"
        ).set_image(
            url = data["reward"]["banner"]
        ))
        
    @_season_command.autocomplete("saison")
    async def _season_autocomplete(self, inter: disnake.CommandInteraction, string: str) -> list:
        seasons = await self.__db.find_documents(Collections.SEASON, {})

        search_seasons = [
            season["name"]
            for season in seasons
            if string.lower() in season["name"].lower()
        ]

        return search_seasons[:25]

def setup(self) -> None:
    self.add_cog(LotteryModule(self))