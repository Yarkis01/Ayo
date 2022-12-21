import disnake, config
from disnake.ext import commands

from utils.logger import logs

embeds = [
    disnake.Embed(
        title       = "❓ Page d'aide",
        description = "Bienvenue sur la page d'aide d'**Ayo <:ayo:1037021125793828874>** !\nIci, tu trouveras toutes les commandes disponibles sur le bot et une description pour expliquer à quoi elles servent. Toutes les commandes commencent par `/`.\n\nTu peux utiliser les boutons ci-dessous pour naviguer de page en page.",
        color       = 0xffffff
    ),
    disnake.Embed(
        title       = "👥 Code-Ami",
        description = "Voici toutes les commandes en rapport avec le système de code-ami:\n\n▫️ `/ca ajouter`: Permet d'ajouter ou de modifier un de ses codes amis\n▫️ `/ca supprimer`: Permet de supprimer un de ses codes amis\n▫️ `/ca liste`: Permet de voir ses codes amis ou celui d'un autre utilisateur\n▫️ `/ca qrcode`: Permet d'obtenir un code ami sous forme de QR Code",
        color       = 0xffffff
    ),
    disnake.Embed(
        title       = "🔄 Rotations",
        description = "Voici toutes les commandes en rapport avec un système de rotation:\n\n▫️ `/rotations actuelles`: Permet d'obtenir la rotation actuelle des stages\n▫️ `/rotations suivantes`: Permet d'obtenir la prochaine rotation des stages\n▫️ `/cephalochic`: Permet de récupérer les équipements disponibles dans la boutique Céphalochic",
        color       = 0xffffff
    ),
    disnake.Embed(
        title       = "ℹ️ Commande d'information",
        description = "Voici toutes les commandes utiles pour obtenir des informations sur le bot:\n\n▫️ `/aide`: Permet d'obtenir la liste des commandes et leurs utilités\n▫️ `/avis`: Donnez votre avis sur le bot\n▫️ `/information`: Permet d'obtenir des informations sur le bot\n▫️ `/inviter`: Permet d'obtenir un lien pour inviter le bot sur son serveur\n▫️ `/ping`: Permet d'obtenir plein d'information (in)utile sur le bot",
        color       = 0xffffff
    ),
    disnake.Embed(
        title       = "<:ayo:1037021125793828874> Autres",
        description = "Voici les autres commandes, qui ne sont actuellement classé dans aucune catégorie:\n\n▫️ `/bo`: Permet de générer un certain nombre de modes de jeu associé avec des stages\n▫️ `/festival`: Permet d'obtenir des informations sur un festival\n▫️ `/liquider`: Permet de liquider un membre du serveur\n▫️ `/odyssee`: Permet d'obtenir des informations sur l'odyssée d'Omar",
        color       = 0xffffff
    )
]

class HelpView(disnake.ui.View):
    def __init__(self, embeds: list) -> None:
        super().__init__(timeout = None)
        self.embeds = embeds
        self.index  = 0

    def _update_state(self) -> None:
        self.prev_page.disabled = self.index == 0
        self.next_page.disabled = self.index == len(self.embeds) - 1

    @disnake.ui.button(emoji="◀", style=disnake.ButtonStyle.blurple)
    async def prev_page(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        self.index -= 1
        self._update_state()

        await inter.response.edit_message(embed=self.embeds[self.index].set_footer(text = "Développer avec ♥️ par Yarkis#0397"), view=self)

    @disnake.ui.button(emoji="🗑️", style=disnake.ButtonStyle.red)
    async def remove(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await inter.response.edit_message(view = None)

    @disnake.ui.button(emoji="▶", style=disnake.ButtonStyle.blurple)
    async def next_page(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        self.index += 1
        self._update_state()

        await inter.response.edit_message(embed = self.embeds[self.index].set_footer(text = "Développer avec ♥️ par Yarkis#0397"), view = self)

class HelpCommandModule(commands.Cog):
    def __init__(self, bot: commands.AutoShardedInteractionBot) ->None:
        self.__bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        logs.success("Le module a été initié correctement", "[HELP-CMD]")

    @commands.slash_command(name = "aide", description = "Permet d'obtenir la liste des commandes et leurs utilités", dm_permission = False)
    async def _help(
        self,
        inter: disnake.CommandInter
    ) -> None:
        await inter.send(embed = embeds[0].set_footer(text = "Développer avec ♥️ par Yarkis#0397"), view = HelpView(embeds), ephemeral = True)

def setup(self) -> None:
    if config.HELPCOMMAND_ENABLED:
        self.add_cog(HelpCommandModule(self))
        logs.info("Le module a bien été détécté et chargé", "[HELP-CMD]")
    else:
        logs.warning("Le module n'a pas été chargé car il est désactivé dans la configuration", "[HELP-CMD]")
