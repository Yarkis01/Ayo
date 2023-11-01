from disnake.ext import commands
import disnake

from utils.config import Config
from utils.embed import Embed
from utils.logger import Logger


class HelpfulView(disnake.ui.View):
    def __init__(self, bot_id: int, support_server: str):
        super().__init__()

        self.add_item(
            disnake.ui.Button(
                label="Ajoutez Ayo",
                emoji="<:ayo:1037021125793828874>",
                url=f"https://ptb.discord.com/api/oauth2/authorize?client_id={bot_id}&permissions=537380928&scope=applications.commands%20bot",
            )
        )
        self.add_item(
            disnake.ui.Button(label="Serveur de Support", emoji="🤝", url=support_server)
        )
        self.add_item(
            disnake.ui.Button(
                label="Code Source",
                emoji="<:github:1088570213064253534>",
                url="https://github.com/Yarkis01/Ayo",
            )
        )


class HelpfulModule(commands.Cog):
    def __init__(self, bot: commands.AutoShardedInteractionBot):
        self.__bot = bot
        self.__config: Config = bot.config

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        Logger.success("The module has been started correctly", "helpful")

    @commands.slash_command(
        name="information",
        description="Obtiens des informations sur le bot",
        dm_permission=False,
    )
    async def _information_command(self, inter: disnake.CommandInteraction) -> None:
        await inter.send(
            embed=Embed.default(
                title="📄 Information",
                description="""**Ayo <:ayo:1037021125793828874>** est un bot orienté **Nintendo** et plus précisément Splatoon <:Splatoon3:1036691272871718963>.
C'est un bot entièrement en **français 🇫🇷**.
Il est développé par un fan pour des fans.

**__Fonctionnalités principales__**:
▫️ Obtenir les rotations actuelles et suivantes des différents jeux Splatoon (*Splatoon <:Splatoon2:1036691271076560936> et <:Splatoon3:1036691272871718963> uniquement*)
▫️ Un système de code ami synchronisé entre tous les serveurs disposant du bot
▫️ Des commandes diverses et variées pour toute utilisation
▫️ Fonctionne entièrement grâce aux *commandes slashs* et aux *commandes utilisateurs*

▪️ **__Vous êtes tenté par le bot ?__**
Qu'attendez-vous pour l'ajouter et vous faire votre propre avis !
▪️ **__Vous avez un problème, une suggestion de fonctionnalité ?__**
Rejoignez le serveur de support et parlez-en !
▪️ **__Vous souhaitez contribuer au développement de Ayo ?__**
Faites un petit tour sur le Github du bot !
Je serais heureux que vous preniez part à cette magnifique aventure.

*Vous pouvez consulter nos **Conditions Générales d'Utilisation** [ici](https://github.com/Yarkis01/Ayo/blob/main/TERMS_OF_USE.md) et notre **Politique de Confidentialité** [ici](https://github.com/Yarkis01/Ayo/blob/main/PRIVACY_POLICY.md). Nous vous encourageons à lire attentivement ces documents pour comprendre nos règles et notre approche en matière de confidentialité.*""",
            ).set_footer(
                text=f"Latence actuelle du bot: {round(self.__bot.latency * 1000)}ms"
            ),
            view=HelpfulView(inter.me.id, self.__config.support_server),
        )

    @commands.slash_command(
        name="inviter",
        description="Vous souhaitez ajouter Ayo à votre serveur ?",
        dm_permission=False,
    )
    async def _invite_command(self, inter: disnake.CommandInteraction) -> None:
        await inter.send(
            embed=Embed.default(
                title="✉️ Excellente idée !",
                description="Voici votre invitation pour pouvoir rajouter **Ayo <:ayo:1037021125793828874>** sur votre propre serveur !\nIl suffit simplement de cliquer sur le bouton en dessous.",
            ).set_footer(
                text=f"Latence actuelle du bot: {round(self.__bot.latency * 1000)}ms"
            ),
            view=HelpfulView(inter.me.id, self.__config.support_server),
        )


def setup(self) -> None:
    self.add_cog(HelpfulModule(self))
