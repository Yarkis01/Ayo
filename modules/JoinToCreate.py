import disnake
from disnake.ext import commands

import config
from utils.logger import logs

class JoinToCreateModule(commands.Cog):
    def __init__(self, bot: commands.AutoShardedInteractionBot) -> None:
        self.__bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        logs.success("Le module a été initié correctement", "[J2C]")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: disnake.Member, before: disnake.VoiceState, after: disnake.VoiceState) -> None:
        if member.bot:
            return

        if member.guild.id not in config.TEST_GUILDS:
            return

        if after.channel is not None:
            if after.channel.id == config.J2C_CHANNEL_02_ID:
                places = 2
            elif after.channel.id == config.J2C_CHANNEL_04_ID:
                places = 4
            elif after.channel.id == config.J2C_CHANNEL_10_ID:
                places = 10
            else:
                return

            new_channel = await after.channel.category.create_voice_channel(f"Vocal de {member}", user_limit = places, reason = f"Création d'un salon pour l'utilisateur {member}")
            await member.move_to(new_channel, reason = f"Déplacement de l'utilisateur dans son salon avec {places} places")
        
        if before.channel is not None and before.channel.id not in [config.J2C_CHANNEL_02_ID, config.J2C_CHANNEL_04_ID, config.J2C_CHANNEL_10_ID] and before.channel.category.id == config.J2C_CATEGORY_ID:
            if len(before.channel.members) == 0:
                await before.channel.delete(reason = "Tous les utilisateurs du salon ont quitté")

def setup(self) -> None:
    if config.JOIN2CREATE_ENABLED:
        self.add_cog(JoinToCreateModule(self))
        logs.info("Le module a bien été détécté et chargé", "[J2C]")
    else:
        logs.warning("Le module n'a pas été chargé car il est désactivé dans la configuration", "[J2C]")