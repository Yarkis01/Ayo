import disnake
from disnake.ext import commands

import config
from utils.logger import logs

class JoinToCreateModule(commands.Cog):
    def __init__(self, bot: commands.AutoShardedInteractionBot) -> None:
        self.__bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        logs.success("Le module a été initié correctement", "[JOIN2CREATE]")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: disnake.Member, before: disnake.VoiceState, after: disnake.VoiceState) -> None:
        if member.bot:
            return

        if member.guild.id != config.GUILD_ID:
            return

        if after.channel is not None:
            if after.channel.id == config.JOIN2CREATE[0]:
                places = 2
            elif after.channel.id == config.JOIN2CREATE[1]:
                places = 4
            elif after.channel.id == config.JOIN2CREATE[2]:
                places = 10
            else:
                return

            new_channel = await after.channel.category.create_voice_channel(f"Vocal de {member}", user_limit = places, reason = f"Création d'un salon pour l'utilisateur {member}")
            await member.move_to(new_channel, reason = f"Déplacement de l'utilisateur dans son salon avec {places} places")
        
        if before.channel is not None and before.channel.id not in config.JOIN2CREATE and before.channel.category.id == config.JOIN2CREATE[3]:
            if len(before.channel.members) == 0:
                await before.channel.delete(reason = "Tous les utilisateurs du salon ont quitté")

def setup(self) -> None:
    self.add_cog(JoinToCreateModule(self))