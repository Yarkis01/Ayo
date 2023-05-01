import disnake, pytz, config, requests, asyncio, contextlib
from disnake.ext import commands, tasks
from datetime import datetime, timedelta

import helper.rotations as RH
import helper.data as HDATA
from utils.logger import logs

CHOICES = {
    "Splatoon 3": "s3", 
    "Splatoon 2": "s2", 
    "Salmon Run (Splatoon 3)": "salmon",
    "Salmon Run (Splatoon 2)": "salmon2",
    "Défi œuf sup' (Splatoon 3)": "oeufsup"
}

class RotationsModule(commands.Cog):
    def __init__(self, bot: commands.AutoShardedInteractionBot) -> None:
        self.__bot = bot
        self.__started = False

        self.__splatoon3_data = None
        self.__splatoon2_data = None

        self.__salmonrun_data   = None
        self.__salmongears_data = None
        self.__salmonrun2_data  = None

        self.__next_rotation            = datetime(2022, 10, 30, 22, 0, 0, 0).astimezone(pytz.timezone(config.TIMEZONE))
        self.__salmonrun3_next_rotation = datetime(2022, 10, 30, 22, 0, 0, 0).astimezone(pytz.timezone(config.TIMEZONE))
        self.__salmonrun2_next_rotation = datetime(2022, 10, 30, 22, 0, 0, 0).astimezone(pytz.timezone(config.TIMEZONE))



    @commands.Cog.listener()
    async def on_ready(self) -> None:
        if not self.__started:
            self.splatoon2_salmonrun_loop.start()
            self.splatoon3_salmonrun_loop.start()
            self.splatoon_loop.start()
        logs.info("Le module est en train d'être initié", "[ROTATIONS]")
        await asyncio.sleep(15)
        self.__started = True
        logs.success("Le module a été initié correctement", "[ROTATIONS]")



    @tasks.loop(seconds = 30)
    async def splatoon_loop(self) -> None:
        now = datetime.now().astimezone(pytz.timezone(config.TIMEZONE))
        if (self.__next_rotation - now) >= timedelta(hours = 0):
            return

        self.__next_rotation = datetime(now.year, now.month, now.day, now.hour, 0, 0, 0).astimezone(pytz.timezone(config.TIMEZONE)) + timedelta(hours = config.ADD_HOURS + 1, minutes = 1, seconds = 5) if now.hour % 2 else datetime(now.year, now.month, now.day, now.hour, 0, 0, 0).astimezone(pytz.timezone(config.TIMEZONE)) + timedelta(hours = config.ADD_HOURS, minutes = 1, seconds = 5)

        try:
            s3_request = requests.get(f"{config.SPLATOON3_API}/schedules.json", headers=config.HEADERS_BASE, timeout = config.TIMEOUT)
            self.__splatoon3_data = s3_request.json()["data"] if s3_request.status_code == 200 else None
        except requests.Timeout:
            self.__splatoon3_data = None

        try:
            s2_request = requests.get(f"{config.SPLATOON2_API}/schedules.json", headers=config.HEADERS_BASE, timeout = config.TIMEOUT)
            self.__splatoon2_data = s2_request.json() if s2_request.status_code == 200 else None
        except requests.Timeout:
            self.__splatoon2_data = None


        if not self.__started:
            return

        embeds = []

        if self.__splatoon3_data is not None:
            HDATA.check_splatoon3_data()
            embeds.append(RH.generate_splatoon3_embed(self.__splatoon3_data, title = "Une nouvelle rotation est disponible !"))
        
        if self.__splatoon2_data is not None:
            embeds.append(RH.generate_splatoon2_embed(self.__splatoon2_data, title = "Une nouvelle rotation est disponible !"))
        
        with contextlib.suppress(Exception):
            channel = await self.__bot.fetch_channel(config.ROTATION_CHANNEL_ID)
            if channel is not None and embeds:
                message = await channel.send(f"<@&{config.ROTATION_ROLES_ID}>", embeds = embeds)
                if channel.type == disnake.channel.NewsChannel:
                    message.publish()


    @tasks.loop(seconds = 30)
    async def splatoon3_salmonrun_loop(self) -> None:
        now = datetime.now().astimezone(pytz.timezone(config.TIMEZONE))
        if (self.__salmonrun3_next_rotation - now) >= timedelta(hours = 0):
            return

        try:
            request = requests.get(f"{config.SPLATOON3_API}/schedules.json", headers = config.HEADERS_BASE, timeout = config.TIMEOUT)
            self.__salmonrun_data = request.json()["data"]["coopGroupingSchedule"] if request.status_code == 200 else None
        except requests.Timeout:
            self.__salmonrun_data = None

        if self.__salmonrun_data is None:
            self.__salmonrun3_next_rotation = datetime(now.year, now.month, now.day, now.hour, 0, 0, 0).astimezone(pytz.timezone(config.TIMEZONE)) + timedelta(hours = 1) 
            return

        self.__salmonrun3_next_rotation = datetime.fromisoformat(self.__salmonrun_data["regularSchedules"]["nodes"][0]["endTime"][:-1]).astimezone(pytz.timezone(config.TIMEZONE)) + timedelta(hours = config.ADD_HOURS, minutes = 1, seconds = 2)
        
        try:
            gears_request           = requests.get(f"{config.SPLATOON3_API}/coop.json", headers = config.HEADERS_BASE, timeout = config.TIMEOUT)
            self.__salmongears_data = gears_request.json()['data']['coopResult']['monthlyGear'] if gears_request.status_code == 200 else None
        except requests.Timeout:
            self.__salmongears_data = None

        if not self.__started:
            return

        HDATA.check_splatoon3_data()

        with contextlib.suppress(Exception):
            channel = await self.__bot.fetch_channel(config.ROTATION_CHANNEL_ID)
            if channel is not None:
                message = await channel.send(f"<@&{config.ROTATION_ROLES_ID}>", embed = RH.generate_salmonrun_embed(self.__salmonrun_data, self.__salmongears_data, title = "Une nouvelle rotation est disponible !", new_rotation = True))
                if channel.type == disnake.channel.NewsChannel:
                    message.publish()


    @tasks.loop(seconds = 30)
    async def splatoon2_salmonrun_loop(self) -> None:
        now = datetime.now().astimezone(pytz.timezone(config.TIMEZONE))
        if (self.__salmonrun2_next_rotation - now) >= timedelta(hours = 0):
            return

        try:
            request                = requests.get(f"{config.SPLATOON2_API}/coop-schedules.json", headers = config.HEADERS_BASE, timeout = config.TIMEOUT)
            self.__salmonrun2_data = request.json() if request.status_code == 200 else None
        except requests.Timeout:
            self.__salmonrun2_data = None

        if self.__salmonrun2_data is None:
            self.__salmonrun2_next_rotation = datetime(now.year, now.month, now.day, now.hour, 0, 0, 0).astimezone(pytz.timezone(config.TIMEZONE)) + timedelta(hours = 1)
            return

        self.__salmonrun2_next_rotation = datetime.fromtimestamp(self.__salmonrun2_data["schedules"][1]["start_time"]).astimezone(pytz.timezone(config.TIMEZONE)) + timedelta(minutes = 1, seconds = 2)

        if not self.__started:
            return

        channel = await self.__bot.fetch_channel(config.ROTATION_CHANNEL_ID)
        if channel is not None:
            message = await channel.send(f"<@&{config.ROTATION_ROLES_ID}>", embed = RH.generate_splatoon2_salmonrun_embed(self.__salmonrun2_data, title = "Une nouvelle rotation est disponible !"))
            if channel.type == disnake.channel.NewsChannel:
                message.publish()


    @commands.slash_command(name = "rotations", description = "Permet d'obtenir des informations sur les rotations", dm_permission = False)
    async def rotations_command(self, inter: disnake.CommandInteraction):
        return

    @rotations_command.sub_command(name = "actuelles", description = "Permet d'obtenir la rotation actuelle des stages")
    async def rotations_actuelles_command(self, inter: disnake.CommandInteraction, data: str = commands.Param(name = "mode", description = "Choisissez le mode que vous souhaitez avoir la rotation", choices = CHOICES)):
        if data == "s3" and self.__splatoon3_data is not None:
            embed = RH.generate_splatoon3_embed(self.__splatoon3_data)
        elif data == "s2" and self.__splatoon2_data is not None:
            embed = RH.generate_splatoon2_embed(self.__splatoon2_data)
        elif data == "salmon" and self.__salmonrun_data is not None:
            embed = RH.generate_salmonrun_embed(self.__salmonrun_data, self.__salmongears_data)
        elif data == "salmon2" and self.__salmonrun2_data is not None:
            embed = RH.generate_splatoon2_salmonrun_embed(self.__salmonrun2_data)
        elif data == "oeufsup" and self.__splatoon3_data is not None:
            embed = RH.generate_defi_oeuf_sup(self.__salmonrun_data)
        else:
            await inter.send(":x: Oups, une erreur est survenue !", ephemeral = True)
            return

        await inter.send(embed = embed)


    @rotations_command.sub_command(name = "suivantes", description = "Permet d'obtenir la prochaine rotation des stages")
    async def prochaines_rotations_command(
        self, 
        inter: disnake.CommandInteraction, 
        data: str = commands.Param(name = "mode", description = "Choisissez le mode que vous souhaitez avoir la rotation", choices = CHOICES),
        number: commands.Range[1, 2] = commands.Param(name = "numéro", description = "Permet d'indiquer le numéro de la prochaine rotation (entre 1 et 2)", default = 1)
    ):
        title = "Rotation suivante" if number == 1 else "Prochaine rotation"
        if data == "s3" and self.__splatoon3_data is not None:
            embed = RH.generate_splatoon3_embed(self.__splatoon3_data, number, title)
        elif data == "s2" and self.__splatoon2_data is not None:
            embed = RH.generate_splatoon2_embed(self.__splatoon2_data, number, title)
        elif data == "salmon" and self.__salmonrun_data is not None:
            embed = RH.generate_salmonrun_embed(self.__salmonrun_data, self.__salmongears_data, number, title)
        elif data =="salmon2" and self.__salmonrun2_data is not None:
            embed = RH.generate_splatoon2_salmonrun_embed(self.__salmonrun2_data, number, title)
        elif data == "oeufsup" and self.__splatoon3_data is not None:
            embed = RH.generate_defi_oeuf_sup(self.__salmonrun_data, number)
        else:
            await inter.send(":x: Oups, une erreur est survenue !", ephemeral = True)
            return

        await inter.send(embed = embed)

def setup(self) -> None:
    self.add_cog(RotationsModule(self))
    logs.info("Le module a bien été détécté et chargé", "[ROTATIONS]")