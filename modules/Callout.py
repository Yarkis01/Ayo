import disnake, json, os, unidecode
from disnake.ext import commands

from utils.logger import logs
from helper.icons import get_ranked_icon

splatoon3_data = json.load(open("./data/s3/stages.json"))
splatoon2_data = json.load(open("./data/s2/stages.json"))

class CalloutModule(commands.Cog):
    def __init__(self, bot: commands.AutoShardedInteractionBot) -> None:
        self.__bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        logs.success("Le module a été initié correctement", "[CALLOUT]")

    @commands.slash_command(name = "callout", dm_permission = False)
    async def _callout(self, inter: disnake.CommandInteraction) -> None:
        return
    
    @_callout.sub_command(name = "splatoon3", description = "Obtenir le plan d'une carte")
    async def _callout_s3(
        self,
        inter: disnake.CommandInteraction,
        stage: str = commands.Param(name = "stage", choices = splatoon3_data["stages"])
    ) -> None:
        await inter.send("Chargement...")

        if stage != "Club Ca$halot":
            await inter.edit_original_response(content = "", embed = disnake.Embed(
                title = f"🗺️ Callout - {stage} - {get_ranked_icon('Expédition risquée')}{get_ranked_icon('Mission Bazookarpe')}{get_ranked_icon('Défense de zone')}{get_ranked_icon('Pluie de Palourdes')}",
                color = 0xebeb3f
            ).set_image("attachment://image.png"), file = disnake.File(f"./data/s3/callout/{unidecode.unidecode(stage.lower().replace(' ', '_'))}.png", "image.png"))
        else:
            await inter.edit_original_response(embeds = [
                disnake.Embed(
                    title       = f"🗺️ Callout - {stage} - {get_ranked_icon('Mission Bazookarpe')}{get_ranked_icon('Pluie de Palourdes')}",
                    description = f"Voici la carte de {stage} pour **Mission Bazookarpe** et **Pluie de palourdes**.",
                    color       = 0xebeb3f
                ).set_image("attachment://image.png"),
                disnake.Embed(
                    title       = f"🗺️ Callout - {stage} - {get_ranked_icon('Expédition risquée')}",
                    description = f"Voici la carte de {stage} pour **Exp\u00E9dition risqu\u00E9e**.",
                    color       = 0xebeb3f
                ).set_image("attachment://expedition_risquee.png"),
                disnake.Embed(
                    title       = f"🗺️ Callout - {stage} - {get_ranked_icon('Défense de zone')}",
                    description = f"Voici la carte de {stage} pour **D\u00E9fense de zone**",
                    color       = 0xebeb3f
                ).set_image("attachment://defense_de_zone.png")
            ], files = [
                disnake.File("./data/s3/callout/club_ca$halot_rm_cb.png", "image.png"),
                disnake.File("./data/s3/callout/club_ca$halot_tc.png", "expedition_risquee.png"),
                disnake.File("./data/s3/callout/club_ca$halot_sz.png", "defense_de_zone.png"),
            ], content = "")

    @_callout.sub_command(name = "splatoon2", description = "Obtenir le plan d'une carte")
    async def _callout_s3(
        self,
        inter: disnake.CommandInteraction,
        stage: str = commands.Param(name = "stage", choices = splatoon2_data["stages"]),
        view : str = commands.Param(name = "vue", choices = {"Mini-map": "map", "Aérienne (par défaut)": "top"}, default = "top")
    ) -> None:
        await inter.send("Chargement...")

        if stage != "Carrières Caviar":
            await inter.edit_original_response(content = "", embed = disnake.Embed(
                title = f"🗺️ Callout - {stage} - {get_ranked_icon('Expédition risquée')}{get_ranked_icon('Mission Bazookarpe')}{get_ranked_icon('Défense de zone')}{get_ranked_icon('Pluie de Palourdes')}",
                color = 0xf03c78
            ).set_image("attachment://image.png"), file = disnake.File(f"./data/s2/callout/{unidecode.unidecode(stage.lower().replace(' ', '_'))}_{view}.png", "image.png"))
        else:
            await inter.edit_original_response(embeds = [
                disnake.Embed(
                    title       = f"🗺️ Callout - {stage} - {get_ranked_icon('Expédition risquée')}{get_ranked_icon('Défense de zone')}{get_ranked_icon('Pluie de Palourdes')}",
                    description = f"Voici la carte de {stage} pour **Expédition risquée**, **Défense de zone** et **Pluie de palourdes**.",
                    color       = 0xf03c78
                ).set_image("attachment://image.png"),
                disnake.Embed(
                    title       = f"🗺️ Callout - {stage} - {get_ranked_icon('Mission Bazookarpe')}",
                    description = f"Voici la carte de {stage} pour **Mission Bazookarpe**.",
                    color       = 0xf03c78
                ).set_image("attachment://bazookarpe.png"),
            ], files = [
                disnake.File(f"./data/s2/callout/carrieres_caviar_{view}.png", "image.png"),
                disnake.File(f"./data/s2/callout/carrieres_caviar_{view}_rm.png", "bazookarpe.png")
            ], content = "")

def setup(self) -> None:
    self.add_cog(CalloutModule(self))
    logs.info("Le module a bien été détécté et chargé", "[CALLOUT]")