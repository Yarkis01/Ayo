import disnake, json, random, secrets
from disnake.ext import commands

import helper.rotations as RH
from utils.logger import logs

BESTOF_NUMBER = [
    1, 3, 5, 7
]

BESTOF_JEUX = {
    "Splatoon 3": "s3",
    "Splatoon 2": "s2",
    "Splatoon": "s1"
}

class BestOfModule(commands.Cog):
    def __init__(self, bot: commands.AutoShardedInteractionBot) -> None:
        self.__bot  = bot
        self.__data = json.load(open("./data/bestof.json"))

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        logs.success("Le module a été initié correctement", "[BOX]")

    async def generate_rotation(self, game: str, stages_data) -> tuple:
        return (
            secrets.choice(self.__data["modes"][game]),
            secrets.choice(stages_data)
        )

    @commands.slash_command(name = "bo", description = "Permet de générer un certain nombre de modes de jeu associé avec des stages", dm_permission = False)
    async def _bo(
        self,
        inter: disnake.CommandInteraction,
        number: int = commands.Param(name = "nombre", description = "Nombre de parties que vous voulez jouer", choices = BESTOF_NUMBER),
        game: str = commands.Param(name = "jeu", description = "Quel jeu va être utilisé pour effectuer ses parties ? (par défaut: Splatoon 3)", choices = BESTOF_JEUX, default = "s3")
    ) -> None:
        stages_data: list = self.__data["stages"][game]
        modes_count: dict = {}
        stage_count: dict = {}
        old_stage: str    = None
        old_mode: str     = None

        description = "Voici les maps sur lesquels vous devez jouer :\n\n"

        i = 0
        while i != number:
            mode, stage = await self.generate_rotation(game, stages_data)
            if mode == old_mode or stage == old_stage:
                continue

            modes_count[mode] = 1 if mode not in modes_count else modes_count[mode] + 1
            stage_count[stage] = 1 if stage not in stage_count else stage_count[stage] + 1

            if modes_count[mode] > 3 or stage_count[stage] > 2:
                continue

            old_mode     = mode
            old_stage    = stage
            description += f"**{RH.get_ranked_icon(mode)} {mode}** sur **{stage}**\n"
            i           += 1

        if number != 1:
            description += f"\nIl faut au moins remporter **{int(number / 2) + 1} matchs** pour décrocher la victoire !"
        description += "\nQue la meilleure équipe gagne !"

        if game == "s3":
            title = "<:Splatoon3:1036691272871718963>"
            color = 0xebeb3f
        elif game == "s2":
            title = "<:Splatoon2:1036691271076560936>"
            color = 0xf03c78
        else:
            title = "<:Splatoon:1036691269256228954>"
            color = 0xffffff
        title += f" Matchs d'entraînement (BO{number})"

        await inter.send(content = "", embed = disnake.Embed(
            title       = title,
            description = description,
            color       = color
        ))


def setup(self) -> None:
    self.add_cog(BestOfModule(self))