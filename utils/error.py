import time
import traceback
import uuid

from disnake.ext import commands
import disnake

from utils.database import Collections
from utils.embed    import Embed
from utils.logger   import Logger

class ErrorView(disnake.ui.View):
    """Represents the error view containing the support server button."""

    def __init__(self, support_server: str):
        super().__init__()
        self.add_item(disnake.ui.Button(label = "Rejoindre le serveur de support", url = support_server, emoji = "🤝"))

async def error_message_generator(
    bot      : commands.AutoShardedInteractionBot,
    inter    : disnake.ApplicationCommandInteraction,
    exception: commands.CommandError
) -> None:
    """
    Generates an error message when a command fails.
    Sends an error message to the user, logs the error, and stores it in the database.
    
    Args:
        bot: The bot instance
        inter: The interaction that triggered the error
        exception: The exception raised
    """
    
    error_code = uuid.uuid4()
    
    await inter.send(embed = Embed.error(
        title        =  ":x: Une erreur est survenue",
        description  =  f"Une erreur est survenue lors de l'exécution de la commande `{inter.application_command.name}`.\n" \
                        f"Veuillez réessayer plus tard, si le problème persiste, rejoignez le serveur de support et donner ce code d'erreur : `{error_code}`"
    ), view = ErrorView(bot.config.support_server),ephemeral = True)
    
    Logger.fail(f"\"{inter.author}\" to encounter an error with the \"{str(inter.application_command.name)}\" command ({error_code})", "error")
    
    await bot.database.insert_document(Collections.ERRORS, {
        "uuid": str(error_code),
        "time": int(time.time()),
        "commands": inter.application_command.name,
        "error": str(exception),

        "author": {
            "id"  : inter.author.id,
            "name": inter.author.name,
            "permissions": inter.author.guild_permissions.value
        },
        "channel": {
            "id"  : inter.channel.id,
            "name": inter.channel.name
        },
        "guild": {
            "id"         : inter.guild.id,
            "name"       : inter.guild.name,
            "owner_id"   : inter.guild.owner_id,
            "permissions": inter.me.guild_permissions.value
        }
    })
    
    await bot.logger.send(embed = Embed.error(
        title       = f":x: {inter.author} a rencontré une erreur",
        description = f"**Code d'erreur:** `{error_code}`\n**Commande:** `{inter.application_command.name}`\n**Erreur:** ```{exception}```",
    ))