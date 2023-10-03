from enum import Enum
from random import randint

from disnake.ext import commands
import disnake

from utils.database import Database, Collections
from utils.logger import Logger


class Colors(Enum):
    DEFAULT = 0xFFFFFF
    SALMON_RUN = 0x0C5A42

    GREEN = 0x799516
    LILAC = 0x4D24A3
    PINK = 0xC83D79
    PURPLE = 0x8C0C7F
    TURQUOISE = 0x319471
    YELLOW = 0xFBD704


class SplatModule(commands.Cog):
    def __init__(self, bot: commands.AutoShardedInteractionBot):
        self.__bot = bot
        self.__db: Database = bot.database

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        Logger.success("The module has been started correctly", "splat")

    async def liquider(self, inter: disnake.Interaction, member: disnake.User) -> None:
        await inter.response.defer()

        count = await self.__db.count_documents(Collections.SPLAT)
        cid = randint(0, count - 1)
        data = await self.__db.find_one(Collections.SPLAT, {"cid": cid})
        weapon = data["weapon"]["fr"]

        match (member.id):
            case self.__bot.user.id:
                message = f"{self.__bot.user.mention} vient de liquider {inter.author.mention} à l'aide d'{weapon} !"
            case inter.author.id:
                message = (
                    f"{inter.author.mention} vient de se liquider à l'aide d'{weapon} !"
                )
            case _:
                message = f"{inter.author.mention} vient de liquider {member.mention} à l'aide d'{weapon} !"

        await inter.send(
            embed=disnake.Embed(
                title="<:liquider:1037043210645667880> Liquidation !",
                description=message,
                color=getattr(Colors, data["color"].upper(), Colors.DEFAULT).value,
            )
            .set_image(url=data["url"])
            .set_footer(
                text=f"L'image ne se charge pas ? Contactez le support pour résoudre ce problème.\nCID: {cid}"
            )
        )

    @commands.slash_command(
        name="liquider", description="Liquide un membre du serveur", dm_permission=False
    )
    async def _splat_command(
        self,
        inter: disnake.CommandInteraction,
        member: disnake.User = commands.Param(
            name="membre", description="Membre que vous souhaitez liquider"
        ),
    ) -> None:
        await self.liquider(inter, member)

    @commands.user_command(name="Liquider", dm_permission=False)
    async def _splat_user_command(
        self, inter: disnake.UserCommandInteraction, member: disnake.User
    ) -> None:
        await self.liquider(inter, member)


def setup(self) -> None:
    self.add_cog(SplatModule(self))
