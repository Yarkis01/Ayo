from typing import List

from datetime import datetime, timedelta
import asyncio
import time

from disnake.ext import commands, tasks
import disnake
import pytz

from utils.config    import Config
from utils.embed     import Embed, RotationsEmbed
from utils.logger    import Logger
from utils.requests  import make_api_request

CHOICES = {
    "Splatoon 3": "s3", 
    "Splatoon 2": "s2", 
    "Salmon Run (Splatoon 3)": "salmon_s3",
    "Salmon Run (Splatoon 2)": "salmon_s2",
    "Défi œuf sup' (Splatoon 3)": "oeufsup",
    "Match Challenge (Splatoon 3)": "challenge"
}
class RotationsModule(commands.Cog):
    def __init__(self, bot: commands.AutoShardedInteractionBot):
        self.__bot            = bot
        self.__config: Config = bot.config
        
        self.__is_started      = False
        self.__timezone        = pytz.timezone(self.__config.timezone)
        self.__rotations_embed = RotationsEmbed(self.__config.timezone)
        
        # Schedules (Splatoon 2 & 3)
        self.__schedules_next_rotation = self.__timezone.localize(datetime(1970, 1, 1, 0, 0, 0, 0))
        self.__s3_data = None
        self.__s2_data = None
        
        # Splatoon 3 - Salmon Run
        self.__s3_salmon_next_rotation = self.__timezone.localize(datetime(1970, 1, 1, 0, 0, 0, 0))
        self.__s3_salmon_old_rotation  = self.__timezone.localize(datetime(1970, 1, 1, 0, 0, 0, 0))
        self.__s3_salmon_data          = None
        self.__s3_salmon_gears_data    = None
        
        # Splatoon 2 - Salmon Run
        self.__s2_salmon_next_rotation = self.__timezone.localize(datetime(1970, 1, 1, 0, 0, 0, 0))
        self.__s2_salmon_old_rotation  = self.__timezone.localize(datetime(1970, 1, 1, 0, 0, 0, 0))
        self.__s2_salmon_data          = None
        
        # Splatoon 3 - Challenge
        self.__s3_event_schedules_next_rotation = self.__timezone.localize(datetime(1970, 1, 1, 0, 0, 0, 0))
        self.__s3_event_schedules_old_rotation  = self.__timezone.localize(datetime(1970, 1, 1, 0, 0, 0, 0))
        self.__s3_event_schedules_data          = None
        

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        Logger.success("The module has been started correctly", "rotations")
        
        if not self.__is_started:
            self._schedules_update_loop.start()
            self._s3_salmon_update_loop.start()
            self._s2_salmon_update_loop.start()
            self._event_schedules_loop.start()
            
            await asyncio.sleep(5)
            self.__is_started = True

        
        
    async def __publish_rotations_message(self, embeds: List[disnake.Embed]) -> None:
        if self.__is_started:
            channel = await self.__bot.fetch_channel(self.__config.rotations_channel)
            if channel and embeds:
                message = await channel.send(f"<@&{self.__config.rotations_role}>", embeds = embeds)
                if channel.type == disnake.ChannelType.news:
                    await message.publish()
    
    @tasks.loop(seconds = 30)
    async def _schedules_update_loop(self) -> None:
        now = self.__timezone.localize(datetime.utcnow())
        
        if(self.__schedules_next_rotation - now) >= timedelta(hours = 0):
            return
        
        self.__schedules_next_rotation = self.__timezone.localize(datetime(now.year, now.month, now.day, now.hour, 1, 30, 0) + timedelta(hours = 2 if now.hour % 2 == 0 else 1))
        
        s3_data = await make_api_request(f"{self.__config.splatoon3_api}/schedules.json")
        s2_data = await make_api_request(f"{self.__config.splatoon2_api}/schedules.json")
        
        embeds = []
        
        if s3_data:
            self.__s3_data = s3_data["data"]
            embeds.append(self.__rotations_embed.get_splatoon3_embed(self.__s3_data, title = "Une nouvelle rotation est disponible !"))
        
        if s2_data:
            self.__s2_data = s2_data
            embeds.append(self.__rotations_embed.get_splatoon2_embed(self.__s2_data, title = "Une nouvelle rotation est disponible !"))

        await self.__publish_rotations_message(embeds)
        
    @tasks.loop(seconds = 30)
    async def _s3_salmon_update_loop(self) -> None:
        now = self.__timezone.localize(datetime.utcnow())
        
        if (self.__s3_salmon_next_rotation - now) >= timedelta(hours = 0):
            return
        
        data  = await make_api_request(f"{self.__config.splatoon3_api}/schedules.json")
        
        if not data:
            self.__s3_salmon_next_rotation = now + timedelta(minutes = 30)
            return
        
        next_rotation  = self.__timezone.localize(datetime.strptime(data["data"]["coopGroupingSchedule"]["regularSchedules"]["nodes"][0]["endTime"], "%Y-%m-%dT%H:%M:%SZ")) + timedelta(minutes = 1, seconds = 30)

        if next_rotation == self.__s3_salmon_old_rotation:
            self.__s3_salmon_next_rotation = now + timedelta(minutes = 30)
            return
        
        self.__s3_salmon_next_rotation = next_rotation
        self.__s3_salmon_old_rotation  = next_rotation
        self.__s3_salmon_data          = data["data"]["coopGroupingSchedule"]
        
        gears_data = await make_api_request(f"{self.__config.splatoon3_api}/coop.json")
        if gears_data:
            self.__s3_salmon_gears_data = gears_data['data']['coopResult']['monthlyGear']
        
        embeds = [self.__rotations_embed.get_splatoon3_salmon_embed(self.__s3_salmon_data, self.__s3_salmon_gears_data, title = "Une nouvelle rotation est disponible !")]
        
        oeuf_sup = self.__rotations_embed.get_defi_oeuf_sup_embed(self.__s3_salmon_data)
        if "Aucune rotation " not in oeuf_sup.description:
            embeds.append(oeuf_sup)
        
        await self.__publish_rotations_message(embeds)


    @tasks.loop(seconds = 30)
    async def _s2_salmon_update_loop(self) -> None:
        now = datetime.fromtimestamp(int(time.time())).astimezone(pytz.timezone(self.__config.timezone))
        
        if (self.__s2_salmon_next_rotation - now) >= timedelta(hours = 0):
            return
        
        data = await make_api_request(f"{self.__config.splatoon2_api}/coop-schedules.json")
        if not data:
            self.__s2_salmon_next_rotation = now + timedelta(minutes = 30)
            return
        
        next_rotation = datetime.fromtimestamp(data["schedules"][1]["start_time"]).astimezone(pytz.timezone(self.__config.timezone)) + timedelta(minutes = 1, seconds = 30)

        if next_rotation == self.__s2_salmon_old_rotation:
            self.__s2_salmon_next_rotation = now + timedelta(minutes = 30)
            return
        
        self.__s2_salmon_next_rotation = next_rotation
        self.__s2_salmon_old_rotation  = next_rotation
        self.__s2_salmon_data          = data
        
        await self.__publish_rotations_message([self.__rotations_embed.get_splatoon2_salmon_embed(self.__s2_salmon_data, title = "Une nouvelle rotation est disponible !")])

    @tasks.loop(seconds = 30)
    async def _event_schedules_loop(self) -> None:
        now = self.__timezone.localize(datetime.utcnow())
        
        if (self.__s3_event_schedules_next_rotation - now) >= timedelta(hours = 0):
            return
        
        data  = await make_api_request(f"{self.__config.splatoon3_api}/schedules.json")
        
        if not data:
            self.__s3_event_schedules_next_rotation = now + timedelta(minutes = 30)
            return
        
        event_schedules = data.get("data", {}).get("eventSchedules", {}).get("nodes", [])
        
        if len(event_schedules) >= 2 and len(event_schedules[1].get("timePeriods", [])) > 0:
            next_rotation = self.__timezone.localize(datetime.strptime(data["data"]["eventSchedules"]["nodes"][1]["timePeriods"][0]["startTime"], "%Y-%m-%dT%H:%M:%SZ")) + timedelta(minutes = 1, seconds = 30)
        else:
            next_rotation = now + timedelta(hours = 6)

        if next_rotation == self.__s3_event_schedules_old_rotation:
            self.__s3_event_schedules_next_rotation = now + timedelta(minutes = 30)
            return
        
        self.__s3_event_schedules_next_rotation = next_rotation
        self.__s3_event_schedules_old_rotation  = next_rotation
        self.__s3_event_schedules_data          = data["data"]["eventSchedules"]
        
        if len(event_schedules) >= 2 and len(event_schedules[1].get("timePeriods", [])) > 0:
            await self.__publish_rotations_message([self.__rotations_embed.get_event_schedules_embed(self.__s3_event_schedules_data)])



    @commands.slash_command(name = "rotations", dm_permission = False)
    async def _rotations_command(self, inter: disnake.CommandInteraction) -> None:
        await inter.response.defer()
        
    @_rotations_command.sub_command(name = "follow", description = "Permet d'être informé automatiquement des prochaines rotations.")
    async def _follow_rotations_command(self, inter: disnake.CommandInteraction, channel: disnake.TextChannel = commands.Param(name = "salon", description = "Salon textuel qui recevra automatiquement les prochaines rotations")) -> None:
        if not inter.author.guild_permissions.administrator:
            await inter.send(embed = Embed.error(title = ":x: Permission refusée", description = "Vous devez posséder la permission administrateur pour utiliser cette commande !"))
            return
        
        news_channel: disnake.NewsChannel = await self.__bot.fetch_channel(self.__config.rotations_channel)
        
        if not news_channel or channel.guild.id != inter.guild.id:
            await inter.send(embed = Embed.error(":x: Une erreur est survenue", description = "Malheureusement, une erreur est survenue, veuillez réessayer dans quelques minutes..."))
            return
        
        if channel.type != disnake.ChannelType.text:
            await inter.send(embed = Embed.error(":x: Type de salon non valide", description = f"Impossible d'activer la rotation automatique pour le salon {channel.mention} (`{channel.type}`), car celui-ci n'est pas un salon textuel.\nPS: les salons de types `news` ne sont pas pris en charge en raison d'une limitation de Discord."))
            return
        
        if not inter.guild.me.guild_permissions.manage_webhooks or not channel.permissions_for(channel.guild.me).manage_webhooks:
            await inter.send(embed = Embed.error(":x: Permission manquante", description = "Impossible d'activer cette option, car le bot ne dispose pas de la permission pour gérer les webhooks.\nPour régler ce problème, merci de donner la permission manquante et de relancer la commande."))
            return

        await news_channel.follow(
            destination = channel,
            reason = f"Rotations automatiques suite à la demande de {inter.author.name}"
        )
        
        await inter.send(embed = Embed.success(
            title = "✅ Succès !",
            description = f"L'option de rotation automatique a été activée avec succès.\nSi vous souhaitez la désactiver, il vous suffit simplement de supprimer l'intégration ajoutée par le bot dans le salon correspondant ({channel.mention})."
        ))
        
    @_rotations_command.sub_command(name = "actuelles", description = "Permet d'obtenir la rotation actuelle des stages")
    async def _current_rotations_command(self, inter: disnake.CommandInteraction, data: str = commands.Param(name = "mode", description = "Choisissez le mode que vous souhaitez avoir la rotation", choices = CHOICES)) -> None:
        embed = None
        
        if data == "s3" and self.__s3_data:
            embed = self.__rotations_embed.get_splatoon3_embed(self.__s3_data)
        elif data == "s2" and self.__s2_data:
            embed = self.__rotations_embed.get_splatoon2_embed(self.__s2_data)
        elif data == "salmon_s3" and self.__s3_salmon_data:
            embed = self.__rotations_embed.get_splatoon3_salmon_embed(self.__s3_salmon_data, self.__s3_salmon_gears_data)
        elif data == "salmon_s2" and self.__s2_salmon_data:
            embed = self.__rotations_embed.get_splatoon2_salmon_embed(self.__s2_salmon_data)
        elif data == "oeufsup" and self.__s3_salmon_data:
            embed = self.__rotations_embed.get_defi_oeuf_sup_embed(self.__s3_salmon_data)
        elif data == "challenge" and self.__s3_event_schedules_data:
            embed = self.__rotations_embed.get_event_schedules_embed(self.__s3_event_schedules_data)
            
        if embed:
            await inter.send(embed = embed)
        else:
            await inter.send(":x: Oups, une erreur est survenue !")
            
    @_rotations_command.sub_command(name = "suivantes", description = "Permet d'obtenir la prochaine rotation des stages")
    async def _next_rotations_command(self, inter: disnake.CommandInteraction, data: str = commands.Param(name = "mode", description = "Choisissez le mode que vous souhaitez avoir la rotation", choices = CHOICES), number: commands.Range[int, 1, 2] = commands.Param(name = "numéro", description = "Permet d'indiquer le numéro de la prochaine rotation (entre 1 et 2)", default = 1)) -> None:
        title = "Rotation suivante" if number == 1 else "Prochaine rotation"
        embed = None
        
        if data == "s3" and self.__s3_data:
            embed = self.__rotations_embed.get_splatoon3_embed(self.__s3_data, number, title)
        elif data == "s2" and self.__s2_data:
            embed = self.__rotations_embed.get_splatoon2_embed(self.__s2_data, number, title)
        elif data == "salmon_s3" and self.__s3_salmon_data:
            embed = self.__rotations_embed.get_splatoon3_salmon_embed(self.__s3_salmon_data, self.__s3_salmon_gears_data, number, title)
        elif data == "salmon_s2" and self.__s2_salmon_data:
            embed = self.__rotations_embed.get_splatoon2_salmon_embed(self.__s2_salmon_data, number, title)
        elif data == "oeufsup" and self.__s3_salmon_data:
            embed = self.__rotations_embed.get_defi_oeuf_sup_embed(self.__s3_salmon_data, number)
        elif data == "challenge" and self.__s3_event_schedules_data:
            embed = self.__rotations_embed.get_event_schedules_embed(self.__s3_event_schedules_data, 1)
            
        if embed:
            await inter.send(embed = embed)
        else:
            await inter.send(":x: Oups, une erreur est survenue !")
        

def setup(self) -> None:
    self.add_cog(RotationsModule(self))