import disnake, config
from disnake.ext import commands

from utils.logger import logs

information = "**Ayo <:ayo:1037021125793828874>** est un bot orienté **Nintendo** et plus précisément Splatoon <:Splatoon3:1036691272871718963>.\nC'est un bot entièrement en **français 🇫🇷**.\nIl est développé par un fan pour des fans.\n\n**__Fonctionnalités principales__**:\n▫️ Obtenir les rotations actuelles et suivantes des différents jeux Splatoon (*Splatoon <:Splatoon2:1036691271076560936> et <:Splatoon3:1036691272871718963> uniquement*)\n▫️ Un système de code ami synchronisé entre tous les serveurs disposant du bot\n▫️ Des commandes diverses et variées pour toute utilisation\n▫️ Fonctionne entièrement grâce aux *commandes slashs* et aux *commandes utilisateurs*\n\n▪️ **__Vous êtes tenté par le bot ?__**\nQu'attendez-vous pour l'ajouter et vous faire votre propre avis !\n▪️ **__Vous avez un problème, une suggestion de fonctionnalité ?__**\nRejoignez le serveur de support et parlez-en !\n▪️ **__Vous souhaitez contribuer au développement de Ayo ?__**\nFaite un petit tour sur le Github du bot !\nJe serais heureux que vous preniez part à cette magnifique aventure."

class InviteViewButton(disnake.ui.View):
    def __init__(self) -> None:
        super().__init__()
        self.add_item(disnake.ui.Button(label = "Ajoutez Ayo", url = config.ADD_BOT_LINK, emoji = "<:ayo:1037021125793828874>"))
        self.add_item(disnake.ui.Button(label = "Serveur de Support", url = config.SUPPORT_SERVER, emoji = "🤝"))
        self.add_item(disnake.ui.Button(label = "Code Source", url = config.GITHUB_LINK, emoji = "<:github:1088570213064253534>"))


class InformationCommandModule(commands.Cog):
    def __init__(self, bot: commands.AutoShardedInteractionBot) -> None:
        self.__bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        logs.success("Le module a été initié correctement", "[INFO-CMD]")

    @commands.Cog.listener()
    async def on_guild_join(self, guild: disnake.Guild) -> None:
        channels = await guild.fetch_channels()

        for channel in channels:
            if channel.type != disnake.ChannelType.text:
                continue

            if channel.permissions_for(guild.me).send_messages:
                await channel.send(embed = disnake.Embed(
                    title = ":wave: Merci d'avoir ajouté le bot !",
                    description = information,
                    color = 0xffffff
                ), view = InviteViewButton())
                break

    @commands.slash_command(name = "information", description = "Obtiens des informations sur le bot", dm_permission = False)
    async def _information(self, inter: disnake.CommandInter) -> None:
        await inter.send(embed = disnake.Embed(
            title = "📄 Information",
            description = information,
            color = 0xffffff
        ).set_footer(text = f"Latence actuelle du bot: {round(self.__bot.latency * 1000)}ms"), view = InviteViewButton())

    @commands.slash_command(name = "inviter", description = "Vous souhaitez ajouter Ayo à votre serveur ?", dm_permission = False)
    async def _invite(self, inter: disnake.CommandInter) -> None:
        await inter.send(embed = disnake.Embed(
            title = "✉️ Excellente idée !",
            description = "Voici votre invitation pour pouvoir rajouter **Ayo <:ayo:1037021125793828874>** sur votre propre serveur !\nIl suffit simplement de cliquer sur le bouton en dessous.",
            color = 0xffffff
        ).set_footer(text = f"Latence actuelle du bot: {round(self.__bot.latency * 1000)}ms"), view = InviteViewButton())

def setup(self) -> None:
    self.add_cog(InformationCommandModule(self))
    logs.info("Le module a bien été détécté et chargé", "[INFO-CMD]")