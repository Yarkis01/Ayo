import disnake, requests, config, datetime, pytz, humanize, math
from disnake.ext import commands, tasks

from utils.logger import logs

def convert_size(size_bytes) -> str:
    if size_bytes == 0:
        return "0 octet"
    size_name = ("octets", "Ko", "Mo", "Go", "To", "Po", "Eo", "Zo", "Yo")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])

class PingModule(commands.Cog):
    def __init__(self, bot: commands.AutoShardedInteractionBot) -> None:
        self.__bot         = bot
        self.__message_id  = None
        self.__usage_json  = None
        self.__uptime_json = None 
        self.__start_time  = datetime.datetime.now().astimezone(pytz.timezone(config.TIMEZONE))
        humanize.activate("fr_FR")

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        self._is_alive.start()
        self._uptime_loop.start()
        logs.success("Le module a été initié correctement", "[PING]")

    @tasks.loop(minutes = 30)
    async def _is_alive(self) -> None:
        channel = await self.__bot.fetch_channel(config.ERROR_CHANNEL_ID)
        now     = datetime.datetime.now().astimezone(pytz.timezone(config.TIMEZONE))
        if channel is not None:
            embed = disnake.Embed(
                title = "❤️ Je suis vivant !",
                description = f"Le bot est en ligne depuis: **{humanize.precisedelta(now - self.__start_time)}**",
                color = disnake.Colour.blurple()
            ).set_footer(text = f"Dernière modification: {now.strftime('%d/%m/%Y à %H:%M:%S')}")
            if self.__message_id is None:
                message = await channel.send(embed = embed)
                self.__message_id = message.id
            else:
                message = await channel.fetch_message(self.__message_id)
                if message is not None:
                    await message.edit(embed = embed)
                else:
                    self.__message_id = None

    @tasks.loop(minutes = 10)
    async def _uptime_loop(self) -> None:
        reponse = requests.get(config.BOT_API_URL, headers = {"Authorization": f"Bearer {config.BOT_API_KEY}"})
        if reponse.status_code == 200:
            self.__usage_json = reponse.json()['attributes']['resources']

        response_watchbot = requests.get(config.WATCHBOT_API_URL, headers = {"AUTH-TOKEN": config.WATCHBOT_API_KEY})
        if response_watchbot.status_code == 200: 
            self.__uptime_json = response_watchbot.json()

    @commands.slash_command(name = "ping", description = "Permet d'obtenir plein d'information (in)utile sur le bot", dm_permission = False)
    async def _uptime(self, inter: disnake.CommandInteraction) -> None:
        await inter.send("Chargement...", ephemeral = True)

        embed = disnake.Embed(
            title       = "📊 Statistiques (in)utile",
            description = "Voici plein d'information fortement (in)utile sur le bot.",
            color       = 0xffffff
        ).add_field(
            name   = "🏓 Latence du bot",
            value  = f"{int(self.__bot.latency * 1000)}ms",
            inline = True
        ).add_field(
            name   = f"<:shard:1038454850846990337> Latence (Shard #{inter.guild.shard_id})",
            value  = f"{int(self.__bot.latencies[inter.guild.shard_id][1] * 1000)}ms",
            inline = True
        ).add_field(
            name   = "🕛 Temps en ligne",
            value  = f"{humanize.precisedelta(datetime.datetime.now().astimezone(pytz.timezone(config.TIMEZONE)) - self.__start_time)}",
            inline = True
        )

        if self.__uptime_json is not None:
            uptime_data = ["7d", "30d", "90d"]
            for i in range(len(uptime_data)):
                uptime = float(self.__uptime_json[uptime_data[i]])
                if uptime < 75.0:
                    name = f"<:red_clock:1038773522106941530> Uptime ({uptime_data[i].replace('d', '')} jours)"
                elif uptime >= 75.0 and uptime < 98.0:
                    name = f"<:orange_clock:1038775657406140467> Uptime ({uptime_data[i].replace('d', '')} jours)"
                else:
                    name = f"<:green_clock:1038775694655758386> Uptime ({uptime_data[i].replace('d', '')} jours)"
                
                embed.add_field(
                    name   = name,
                    value  = f"{uptime} %",
                    inline = True
                )

        if self.__usage_json is not None:
            embed.add_field(
                name   = "<:cpu:1038771595164012545> CPU",
                value  = f"{self.__usage_json['cpu_absolute']} %",
                inline = True
            ).add_field(
                name   = "<:ram:1038771604622168194> Mémoire Vive",
                value  = convert_size(self.__usage_json['memory_bytes']),
                inline = True
            ).add_field(
                name   = "<:hdd:1038771601468043385> Espace Disque",
                value  = convert_size(self.__usage_json['disk_bytes']),
                inline = True
            )

        await inter.edit_original_response(content = "", embed = embed.set_footer(text = "Données actualisées toutes les 10 minutes"))

def setup(self) -> None:
    self.add_cog(PingModule(self))