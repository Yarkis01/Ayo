import contextlib

from prettytable import PrettyTable
from disnake.ext import commands
import disnake

from utils.database import Collections, Database
from utils.embed    import Embed
from utils.logger   import Logger

class OdysseeView(disnake.ui.View):
    message: disnake.Message
    
    def __init__(self, table: str):
        super().__init__(timeout = 30.0)
        self.__table = table
        
    async def on_timeout(self) -> None:
        self.show_table_button.disabled = True
        with contextlib.suppress(disnake.NotFound):
            await self.message.edit(view = self)
        
    @disnake.ui.button(label = "Afficher le tableau de données", emoji = "<:odyssee:1038067635839057920>", style = disnake.ButtonStyle.blurple)
    async def show_table_button(self, button: disnake.ui.Button, inter: disnake.MessageInteraction) -> None:
        self.show_table_button.disabled = True
        await inter.response.edit_message(view = self)
        await inter.message.reply(f"```\n{self.__table}```")
        self.stop()
    

class OdysseeModule(commands.Cog):
    def __init__(self, bot: commands.AutoShardedInteractionBot):
        self.__bot          = bot
        self.__db: Database = bot.database
        
    @commands.Cog.listener()
    async def on_ready(self) -> None:
        Logger.success("The module has been started correctly", "odyssee")

    @commands.slash_command(name = "odyssee", description = "Permet d'obtenir des informations sur l'odyssée d'Omar", dm_permission = False)
    async def _odyssee_command(self, inter: disnake.CommandInteraction, voyage: str = commands.Param(name = "voyage", description = "Sur quelle voyage d'Omar voulez vous avoir des informations ?")) -> None:
        await inter.response.defer()
        
        data = await self.__db.find_one(Collections.ODYSSEE, {"name": voyage})
        if not data:
            await inter.send(embed = Embed.error(":x: Voyage invalide", "Merci de bien vouloir préciser un voyage valide."))
            return
        
        table        = PrettyTable(["Numéro", "Points", "Nom", "Récompense"])
        total_points = 0
        for challenge in data["challenges"]:
            table.add_row([challenge['id'], challenge['points'], challenge['name'], challenge['reward']])
            total_points += challenge['points']
            
        view = OdysseeView(table.get_string())
        await inter.send(embed = Embed.default(
            title       = f"<:odyssee:1038067635839057920> L'odyssée d'Omar - {voyage}",
            description = f"Il faut un total de **{f'{total_points:,}'.replace(',', ' ')}** points pour terminer ce voyage.\nLa récompense pour avoir fini ce voyage est : **{data['reward']['name']}**"
        ).set_image(data["image"]).set_thumbnail(data["reward"]["image"]), view = view)
        view.message = await inter.original_message()
        
    @_odyssee_command.autocomplete("voyage")
    async def _odyssee_autocomplete(self, inter: disnake.CommandInteraction, string: str) -> list:
        voyages = await self.__db.find_documents(Collections.ODYSSEE, {})
        return [voyage["name"] for voyage in voyages if string.lower() in voyage["name"].lower()][:25]

def setup(self):
    self.add_cog(OdysseeModule(self))