import disnake, json, config
from disnake.ext import commands

from utils.logger import logs

data = json.load(open("./data/festivals.json"))

def get_position_icon(position: int) -> str:
    if   position == 1:
        return "🥇"
    elif position == 2:
        return "🥈"
    else:
        return "🥉"

class FestivalsModule(commands.Cog):
    def __init__(self, bot: commands.AutoShardedInteractionBot) -> None:
        self.__bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        logs.success("Le module a été initié correctement", "[FESTIVALS]")

    @commands.slash_command(name = "festival", description = "Permet d'obtenir des informations sur un festival", dm_permission = False)
    async def _festival(
        self, 
        inter: disnake.CommandInteraction,
        festival: str = commands.Param(name = "festival", description = "Choisissez le festival sur lequel vous souhaitez obtenir des informations", choices = data['choices'])
    ) -> None:
        festival_data = data["festival"][festival]

        embed = disnake.Embed(
            title       = f"<:splatfest:1040780648341848115> {festival_data['name']}",
            description = f"Date du début: <t:{festival_data['date']['start']}:F>\nDate de fin: <t:{festival_data['date']['end']}:F>\nÉquipe gagnante: **{festival_data['winner']['team']}**",
            color       = disnake.Colour.from_rgb(festival_data['color'][0], festival_data['color'][1], festival_data['color'][2])
        ).set_thumbnail(
            url = festival_data['winner']['image']
        ).set_image(
            url = festival_data['image']
        )

        for i in range(len(festival_data['team'])):
            team_data = festival_data['team'][i]
            if festival in {"0", "1"}:
                embed.add_field(
                    name   = f"{get_position_icon(team_data['position'])} {team_data['name']}",
                    value  = f"- <:conques:1042508259938013264> Conques: **{team_data['result']['conques']}**\n- 🗳️ Votes: **{team_data['result']['votes']}**\n- 🔫 Contributions (ouvert): **{team_data['result']['ouvert']}**\n- 🏆 Contributions (défi): **{team_data['result']['defi']}**",
                    inline = False
                )
            else:
                embed.add_field(
                    name   = f"{get_position_icon(team_data['position'])} {team_data['name']}",
                    value  = f"- <:conques:1042508259938013264> Conques: **{team_data['result']['conques']}**\n- 🗳️ Votes: **{team_data['result']['votes']}**\n- 🔫 Contributions (ouvert): **{team_data['result']['ouvert']}**\n- 🏆 Contributions (défi): **{team_data['result']['defi']}**\n- <:splatfest:1040780648341848115> Match Tricolore: **{team_data['result']['tricolore']}**",
                    inline = False
                )

        await inter.send(embed = embed)

def setup(self) -> None:
    if config.FESTIVALS_ENABLED:
        self.add_cog(FestivalsModule(self))
        logs.info("Le module a bien été détécté et chargé", "[FESTIVALS]")
    else:
        logs.warning("Le module n'a pas été chargé car il est désactivé dans la configuration", "[FESTIVALS]")
