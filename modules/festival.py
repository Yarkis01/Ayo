from disnake.ext import commands
import disnake

from utils.database import Collections, Database
from utils.embed    import Embed
from utils.logger   import Logger

class FestivalModule(commands.Cog):
    def __init__(self, bot: commands.AutoShardedInteractionBot) -> None:
        self.__bot          = bot
        self.__db: Database = bot.database
        
    @commands.Cog.listener()
    async def on_ready(self) -> None:
        Logger.success("The module has been started correctly", "festivals")

    @commands.slash_command(name = "festival", description = "Permet d'obtenir des informations sur un festival (Splatoon 3)", dm_permission = False)
    async def _festival_command(self, inter: disnake.CommandInteraction, festival: str = commands.Param(name = "festival", description = "Choisissez le festival sur lequel vous souhaitez obtenir des informations")) -> None:
        await inter.response.defer()
        
        data = await self.__db.find_one(Collections.FESTIVALS, {"name": festival})
        if not data: 
            await inter.send(embed = Embed.error(":x: Festival invalide", "Merci de bien vouloir préciser un festival valide."))
            return
        
        embed = Embed.default(
            title = f"<:splatfest:1040780648341848115> {data['name']}",
            description = f"Début: <t:{data['date']['start']}:F>\nFin: <t:{data['date']['end']}:F>"
        ).set_thumbnail(
            url = data["winner"]["image"]
        ).set_image(
            url = data["image"]
        )
        
        for team in data["team"]:
            embed.add_field(
                name   = f"🏆 {team['name']} l'emporte !" if team['name'] == data['winner']['team'] else team['name'],
                value  = f"""- <:conques:1042508259938013264> Conques: **{team['result']['conques']:.2f}%**
- 🗳️ Votes: **{team['result']['votes']:.2f}%**
- 🔫 Contributions (ouvert): **{team['result']['ouvert']:.2f}%**
- 🏆 Contributions (défi): **{team['result']['defi']:.2f}%**
{f'- <:tricolore:1134914815375183882> Match Tricolore: **{team["result"]["tricolore"]}**%' if team['result']['tricolore'] else ''}""",
                inline = False
            )
        
        await inter.send(embed = embed)

    @_festival_command.autocomplete("festival")
    async def _festival_autocomplete(self, inter: disnake.CommandInteraction, string: str) -> list:
        festivals = await self.__db.find_documents(Collections.FESTIVALS, {"game": 3})
        return [festival["name"] for festival in festivals if string.lower() in festival["name"].lower()][:25]

def setup(self) -> None:
    self.add_cog(FestivalModule(self))