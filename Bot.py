import sys ; sys.dont_write_bytecode = True

import disnake, os, random, string, traceback
from disnake.ext import commands

import config
from utils.logger import logs

class ErrorView(disnake.ui.View):
    def __init__(self) -> None:
        super().__init__()
        self.add_item(disnake.ui.Button(label = "Rejoindre le serveur de support", url = config.SUPPORT_SERVER, emoji = "🤝"))

class JoinServerView(disnake.ui.View):
    def __init__(self, code: str) -> None:
        super().__init__()
        self.add_item(disnake.ui.Button(label = "Rejoindre le serveur", url = f"https://discord.gg/{code}"))

class AyoBot(commands.AutoShardedInteractionBot):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    async def on_connect(self) -> None:
        logs.success(f"Connecté en tant que {self.user}")

    async def on_ready(self) -> None:
        await self.change_presence(
            activity = disnake.Activity(
                type = 0, name = f"Splatoon 3 | v{config.VERSION}"
            )
        )

        channel = await self.fetch_channel(config.LOGS_CHANNEL_ID)
        if channel is not None:
            await channel.send(embed = disnake.Embed(
                title = ":robot: Bot paré au combat !",
                description = "Je suis prêt frérot, apprends moi à liquider.",
                color = disnake.Colour.green()
            ))
    
    @commands.Cog.listener()
    async def on_guild_join(self, guild: disnake.Guild) -> None:
        channels = await guild.fetch_channels()

        invite = None
        for channel in channels:
            if channel.type != disnake.ChannelType.text:
                continue

            if channel.permissions_for(guild.me).create_instant_invite:
                invite = await channel.create_invite()
                break
        
        channel = await self.fetch_channel(config.LOGS_CHANNEL_ID)
        if channel is not None:
            if invite is not None:
                view = JoinServerView(invite.code)
            else:
                view = None
            
            await channel.send(embed = disnake.Embed(
                title       = "📈 Le bot a rejoint un nouveaux serveur !",
                description = f"Le bot est à présent sur {len(self.guilds)} serveurs",
                color       = 0xffffff
            ), view = view)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: disnake.Guild) -> None:
        channel = await self.fetch_channel(config.LOGS_CHANNEL_ID)
        if channel is not None:
            await channel.send(embed = disnake.Embed(
                title       = "📉 Le bot a été retiré d'un serveur !",
                description = f"Le bot est à présent sur {len(self.guilds)} serveurs",
                color       = 0xffffff
            ))

    async def error_message_generator(self, inter: disnake.ApplicationCommandInteraction, error: commands.CommandError) -> None:
        error_code = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(16))

        logs.fail(f'{inter.author} a rencontré une erreur ({error_code})', f'[ERROR] {str(inter.application_command.name)}')

        await inter.send(embed = disnake.Embed(
            title = ":x: Une erreur est survenue",
            description = f"Une erreur est survenue lors de l'exécution de la commande `{inter.application_command.name}`.\nVeuillez réessayer plus tard, si le problème persiste, rejoignez le serveur de support et donner ce code d'erreur : `{error_code}`",
            color = disnake.Colour.red()
        ), ephemeral = True, view = ErrorView())

        channel = await self.fetch_channel(config.LOGS_CHANNEL_ID)
        if channel is not None:
            await channel.send(embed = disnake.Embed(
                title = f":x: {inter.author} a rencontré une erreur",
                description = f"**Code d'erreur:** `{error_code}`\n**Commande:** `{inter.application_command.name}`\n**Erreur:** ```{error}```",
                color = disnake.Colour.red()
            ))

    async def on_slash_command_error(self, inter: disnake.ApplicationCommandInteraction, error: commands.CommandError) -> None:
        await self.error_message_generator(inter, error)

    async def on_user_command_error(self, inter: disnake.ApplicationCommandInteraction, error: commands.CommandError) -> None:
        await self.error_message_generator(inter, error)

    async def on_error(self, *args, **kwargs) -> None:
        logs.fail('Une erreur est survenue', '[ERROR]')

        channel = await self.fetch_channel(config.LOGS_CHANNEL_ID)
        if channel is not None:
            await channel.send(embed = disnake.Embed(
                title = ":x: Une erreur est survenue",
                description = f"Args: ```{args}```\nKwargs: ```{kwargs}```\nErreur: ```{traceback.format_exc()}```",
                color = disnake.Colour.red()
            ))

if __name__ == '__main__':
    bot = AyoBot(
        intents     = disnake.Intents.default(),
        test_guilds = config.TEST_GUILDS if config.DEV_MODE else None
    )

    for file in os.listdir('./modules'):
        if file.endswith('.py'):
            bot.load_extension(f'modules.{file[:-3]}')
            #logs.info(f"Le module {file[:-3]} a bien été détécté et chargé")

    bot.run(config.DISCORD_TOKEN)