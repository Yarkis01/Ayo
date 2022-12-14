import disnake, config
from disnake.ext import commands

from utils.logger import logs

class FeedbackModal(disnake.ui.Modal):
    def __init__(self) -> None:
        components = [
            disnake.ui.TextInput(
                label       = "Comment avez-vous connu le bot ?",
                custom_id   = "known",
                style       = disnake.TextInputStyle.short,
                min_length  = 1,
                max_length  = 50,
                required    = True
            ),
            disnake.ui.TextInput(
                label       = "Une note entre 1 et 10 :",
                custom_id   = "rate",
                style       = disnake.TextInputStyle.short,
                min_length  = 1,
                max_length  = 2,
                required    = True
            ),
            disnake.ui.TextInput(
                label       = "Votre avis sur le bot",
                custom_id   = "feedback",
                style       = disnake.TextInputStyle.paragraph,
                min_length  = 5,
                max_length  = 512,
                required    = True
            ),
            disnake.ui.TextInput(
                label       = "Recommanderiez-vous le bot et pourquoi ?",
                custom_id   = "recommend",
                style       = disnake.TextInputStyle.paragraph,
                min_length  = 5,
                max_length  = 256,
                required    = True
            )
        ]
        super().__init__(title = "Avis", custom_id = "bot_feedback", components = components)

    async def callback(self, inter: disnake.ModalInteraction) -> None:
        known     = inter.text_values['known']
        rate      = inter.text_values['rate']
        feedback  = inter.text_values['feedback']
        recommend = inter.text_values['recommend']

        channel = await inter.bot.fetch_channel(config.LOGS_CHANNEL_ID)
        if channel is not None:
            await channel.send(embed = disnake.Embed(
                title       = "🌟 Un nouvelle avis !",
                description = f"**{inter.author}** (*ID: {inter.author.id}*) vient de donner son avis sur le bot !\n\nComment avez vous connu le bot ?\n```{known}```\nNote: \n```{rate}```\nAvis: \n```{feedback}```\nRecommandation: \n```{recommend}```",
                color       = disnake.Colour.yellow()
            ))
            await inter.send("Votre avis a été envoyé avec succès.", ephemeral = True)
        else:
            await inter.send("Une erreur est survenue lors de l'envoi de votre message. Veuillez réessayer.", ephemeral = True)

    async def on_error(self, error: Exception, inter: disnake.ModalInteraction) -> None:
        logs.fail(f"{inter.author} a rencontré une erreur.", "[FEEDBACK]")

        channel = await inter.bot.fetch_channel(config.LOGS_CHANNEL_ID)
        if channel is not None:
            channel.send(embed = disnake.Embed(
                title       = f":x: {inter.author} a rencontré une erreur",
                description = f"**Erreur:** ```{error}```",
                color       = disnake.Colour.red()
            ))

        await inter.send(":x: Oups, une erreur est survenue !", ephemeral = True)

class FeedbackView(disnake.ui.View):
    def __init__(self) -> None:
        super().__init__()

        self.add_item(disnake.ui.Button(label = "Top.gg", url = "https://top.gg/bot/1036668894976425994#reviews"))
        self.add_item(disnake.ui.Button(label = "DBL", url = "https://discordbotlist.com/bots/ayo"))

class FeedbackModule(commands.Cog):
    def __init__(self, bot: commands.AutoShardedInteractionBot) -> None:
        self.__bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        logs.success("Le module a été initié correctement", "[FEEDBACK]")

    @commands.slash_command(name = "avis", description = "Donnez votre avis sur le bot", dm_permission = False)
    async def _feedback(self, inter: disnake.CommandInteraction) -> None:
        await inter.response.send_modal(modal = FeedbackModal())
        await inter.send(embed = disnake.Embed(
            title       = "🌟 Votre avis compte pour nous !",
            description = "Votre avis compte pour nous, alors n'hésitez pas à le partager au maximum de personne.\nVous pouvez aussi poster votre message sur les sites de référencements.",
            color       = disnake.Colour.yellow()
        ), view = FeedbackView(), ephemeral = True)


def setup(self) -> None:
    if config.FEEDBACK_ENABLED:
        self.add_cog(FeedbackModule(self))
        logs.info("Le module a bien été détécté et chargé", "[FEEDBACK]")
    else:
        logs.warning("Le module n'a pas été chargé car il est désactivé dans la configuration", "[FEEDBACK]")