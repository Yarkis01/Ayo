from base64 import b64decode
import random
import json

from disnake.ext import commands, tasks
import disnake

from utils.icons import get_rule_icon
from utils.logger import Logger


class BoxModule(commands.Cog):
    def __init__(self, bot: commands.AutoShardedInteractionBot):
        self.__bot = bot

        self.__s2_stages = []
        self.__s2_rules = []
        self.__s3_stages = []
        self.__s3_rules = []
        self.__is_started = False

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        if not self.__is_started:
            self._update_data.start()
            self.__is_started = True

        Logger.success("The module has been started correctly", "BOX")

    @tasks.loop(hours=1)
    async def _update_data(self) -> None:
        splatoon2_data = json.load(open("./data/s2/translation.json"))
        splatoon3_data = json.load(open("./data/s3/translation.json"))

        self.__s2_rules = [
            rule[1]["name"]
            for rule in list(splatoon2_data["rules"].items())
            if rule[1]["name"] != "Guerre de territoire"
        ]
        self.__s3_rules = [
            rule[1]["name"]
            for rule in list(splatoon3_data["rules"].items())
            if rule[0] != "undefined" and rule[1]["name"] != "Guerre de territoire"
        ]

        self.__s2_stages = [
            stage[1]["name"]
            for stage in list(splatoon2_data["stages"].items())
            if int(stage[0]) < 100
        ]
        self.__s3_stages = [
            stage[1]["name"]
            for stage in list(splatoon3_data["stages"].items())
            if "VsStage" in b64decode(stage[0]).decode("utf-8")
        ]

    async def generate_rotation(self, game: int) -> tuple:
        if game == 3:
            return random.SystemRandom().choice(
                self.__s3_rules
            ), random.SystemRandom().choice(self.__s3_stages)
        else:
            return random.SystemRandom().choice(
                self.__s2_rules
            ), random.SystemRandom().choice(self.__s2_stages)

    @commands.slash_command(
        name="bo",
        description="Permet de générer un certain nombre de modes de jeu associé avec des stages",
        dm_permission=False,
    )
    async def _bo_command(
        self,
        inter: disnake.CommandInteraction,
        number: commands.Range[int, 1, 10] = commands.Param(
            name="nombre", description="Nombre de parties que vous voulez jouer"
        ),
        game: int = commands.Param(
            name="jeu",
            description="Quel jeu va être utilisé pour effectuer ses parties ?",
            choices={"Splatoon 2": 2, "Splatoon 3": 3},
            default=3,
        ),
    ) -> None:
        await inter.response.defer()

        rules_count = {}
        stages_count = {}
        old_rule = None
        old_stage = None

        description = "Voici les maps sur lesquels vous devez jouer :\n\n"

        i = 0
        while i != number:
            rule, stage = await self.generate_rotation(game)
            if rule == old_rule or stage == old_stage:
                continue

            rules_count[rule] = rules_count.get(rule, 0) + 1
            stages_count[stage] = stages_count.get(stage, 0) + 1

            if (
                (number > 6 and rules_count[rule] > 3)
                or (number <= 6 and rules_count[rule] > 2)
                or stages_count[stage] > 2
            ):
                continue

            old_rule = rule
            old_stage = stage
            description += f"**{get_rule_icon(rule)} {rule}** sur **{stage}**\n"
            i += 1

        if number != 1:
            description += f"\nIl faut au moins remporter **{number // 2 + 1} matchs** pour décrocher la victoire !"
        description += "\nQue la meilleure équipe gagne !"

        await inter.send(
            embed=disnake.Embed(
                title=f"{'<:Splatoon3:1036691272871718963>' if game == 3 else '<:Splatoon2:1036691271076560936>'} Matchs d'entraînement (BO{number})",
                description=description,
                color=0xEBEB3F if game == 3 else 0xF03C78,
            ).set_footer(
                text="Les rotations générées par cette commande ne sont pas aléatoires à 100 %"
            )
        )


def setup(self) -> None:
    self.add_cog(BoxModule(self))
