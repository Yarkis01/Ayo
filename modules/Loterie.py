import disnake, json
from disnake.ext import commands

from utils.logger import logs

saison_data = json.load(open('./data/s3/saison.json'))

class LoterieModule(commands.Cog):
    def __init__(self, bot: commands.AutoShardedInteractionBot):
        self.__bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        logs.success("Le module a été initié correctement", "[LOTERIE]")

    @commands.slash_command(name = "loterie", dm_permission = False)
    async def loterie_command(self, inter: disnake.CommandInteraction) -> None:
        return
    
    @loterie_command.sub_command("capsulomate", description = "Obtiens les probabilités du Capsulomate")
    async def _capsulomate(self, inter: disnake.CommandInteraction) -> None:
        await inter.send(file = disnake.File("./data/s3/loterie/capsulomate.png"))

    @loterie_command.sub_command("boîte-mystère", description = "Obtiens les probabilités des boîtes mystères")
    async def _mystery_box(
        self, 
        inter: disnake.CommandInteraction,
        catalog: str = commands.Param(name = "catalogue", choices = {"Initial": "catalogue", "Bonus": "catalogue_bonus"})
    ) -> None:
        await inter.send(file = disnake.File(f"./data/s3/loterie/boite-mystere_{catalog}.png"))

    @loterie_command.sub_command("saison", description = "Obtiens les titres et les bannières rares de chaque saison")
    async def _saison_rare_items(
        self, 
        inter: disnake.CommandInteraction,
        choice: str = commands.Param(name = "saison", choices = saison_data["choices"])
    ) -> None:
        data = saison_data["saisons"][choice]

        endDate = f"<t:{data['date']['end']}:d>" if data["date"]["end"] else "*Pas encore terminée*"

        embed = disnake.Embed(
            title       = data["name"],
            description = f"**Début de saison**: <t:{data['date']['start']}:d>\n**Fin de saison**: {endDate}",
            color       = 0xffffff
        ).add_field(
            name  = "<:titre:1096453724219641931> Titre",
            value = data["title"]
        ).set_image(
            url = data["banner"]
        )

        await inter.send(embed = embed)

def setup(self) -> None:
    self.add_cog(LoterieModule(self))
    logs.info("Le module a bien été détécté et chargé", "[LOTERIE]")