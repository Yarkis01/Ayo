import disnake, random, json, config
from disnake.ext import commands

from utils.logger import logs

class SplattedModule(commands.Cog):
    def __init__(self, bot: commands.AutoShardedInteractionBot) -> None:
        self.__bot = bot
        self.__splatted_data = json.load(open("./data/splatted.json"))

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        logs.success("Le module a été initié correctement", "[SPLATTED]")

    async def liquider(self, inter, member: disnake.Member) -> None:
        number = random.randint(0, len(self.__splatted_data["images"]) - 1)
        data = self.__splatted_data["images"][number]

        if member.id == self.__bot.user.id:
            message = f"{self.__bot.user.mention} vient de liquider {inter.author.mention} à l'aide d'{data['weapon']} !"
        elif inter.author.id == member.id:
            message = f"{inter.author.mention} vient de se liquider à l'aide d'{data['weapon']}!"
        else:
            message = f"{inter.author.mention} vient de liquider {member.mention} à l'aide d'{data['weapon']} !"

        await inter.send(embed = disnake.Embed(
            title = "<:liquider:1037043210645667880> Liquidation !",
            description = message,
            color = disnake.Colour.from_rgb(data["color"][0], data["color"][1], data["color"][2])
        ).set_image(data["url"]))

    @commands.slash_command(name = "liquider", description = "Liquide un membre du serveur", dm_permission = False)
    async def liquider_slash_command(self, inter: disnake.CommandInter, member: disnake.Member = commands.Param(name = "membre", description = "Membre que vous souhaitez liquider")) -> None:
        await self.liquider(inter, member)

    @commands.user_command(name = "Liquider")
    async def liquider_user_command(self, inter: disnake.UserCommandInteraction, member: disnake.Member) -> None:
        await self.liquider(inter, member)

def setup(self) -> None:
    if config.SPLATTED_ENABLED:
        self.add_cog(SplattedModule(self))
        logs.info("Le module a bien été détécté et chargé", "[SPLATTED]")
    else:
        logs.warning("Le module n'a pas été chargé car il est désactivé dans la configuration", "[SPLATTED]")