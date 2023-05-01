import disnake, json
from disnake.ext import commands
from prettytable import PrettyTable

from utils.logger import logs

data = json.load(open('./data/s3/odyssee.json'))

class OdysseeView(disnake.ui.View):
    message: disnake.Message

    def __init__(self, table: str):
        super().__init__(timeout = 30.0)
        self.__table = table

    async def on_timeout(self) -> None:
        self.show_table_button.disabled = True
        await self.message.edit(view = self)

    @disnake.ui.button(label = "Afficher le tableau de données", emoji = "<:odyssee:1038067635839057920>", style = disnake.ButtonStyle.blurple)
    async def show_table_button(self, button: disnake.ui.Button, inter: disnake.MessageInteraction) -> None:
        self.show_table_button.disabled = True
        await inter.response.edit_message(view = self)

        await inter.message.reply(f"```\n{self.__table}\n```")

        self.stop()

class OdysseeModule(commands.Cog):
    def __init__(self, bot: commands.AutoShardedInteractionBot) -> None:
        self.__bot  = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        logs.success("Le module a été initié correctement", "[ODYSSÉE]")

    @commands.slash_command(name = "odyssee", description = "Permet d'obtenir des informations sur l'odyssée d'Omar", dm_permission = False)
    async def _odyssee(
        self, 
        inter: disnake.CommandInteraction,
        voyage: str = commands.Param(name = "voyage", description = "Sur quelle voyage d'Omar voulez vous avoir des informations ?", choices = data["choices"])
    ) -> None:
        table = PrettyTable()
        table.field_names = ["Numéro", "Points", "Nom", "Récompense"]
        total_points = 0
        for i in range(len(data[voyage]['challenges'])):
            table.add_row([
                data[voyage]['challenges'][i]['id'],
                data[voyage]['challenges'][i]['points'],
                data[voyage]['challenges'][i]['name'],
                data[voyage]['challenges'][i]['reward']
            ])
            total_points += data[voyage]['challenges'][i]['points']

        view = OdysseeView(table)

        await inter.send(embed = disnake.Embed(
            title = f"<:odyssee:1038067635839057920> L'odyssée d'Omar - Voyage {voyage.replace('v', '')}",
            description = f"Il faut un total de **{total_points} points** pour terminer ce voyage.\nLa récompense pour avoir fini ce voyage est : **{data[voyage]['reward']['name']}**",
            color = 0xffffff
        )
            .set_image(data[voyage]['image'])
            .set_thumbnail(data[voyage]['reward']['image']
        ), view = view)

        view.message = await inter.original_response()

def setup(self) -> None:
    self.add_cog(OdysseeModule(self))
    logs.info("Le module a bien été détécté et chargé", "[ODYSSÉE]")