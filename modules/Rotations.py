import disnake, pytz, config, requests, asyncio, contextlib
from disnake.ext import commands, tasks
from datetime import datetime, timedelta

import helper.rotations as RH
import helper.data as HDATA
from utils.logger import logs

CHOICES = {
    "Splatoon 3": "s3", 
    "Splatoon 2": "s2", 
    "Salmon Run (Splatoon 3)": "salmon"
}

class RotationsModule(commands.Cog):
    def __init__(self, bot: commands.AutoShardedInteractionBot) -> None:
        self.__bot = bot
        self.__started = False

        self.__splatoon3_data = None
        self.__splatoon2_data = None
        self.__salmonrun_data = None
        self.__salmongears_data = None

        self.__next_rotation = datetime(2022, 10, 30, 22, 0, 0, 0).astimezone(pytz.timezone(config.TIMEZONE))

        self.__salmon_start_time = datetime(2022, 10, 30, 20, 0, 0, 0).astimezone(pytz.timezone(config.TIMEZONE))
        self.__salmon_end_time   = datetime(2022, 10, 30, 22, 0, 0, 0).astimezone(pytz.timezone(config.TIMEZONE))

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        if not self.__started:
            self.salmonrun_loop.start()
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

        self.__next_rotation = datetime(now.year, now.month, now.day, now.hour, 0, 0, 0).astimezone(pytz.timezone(config.TIMEZONE)) + timedelta(hours=2, minutes=1, seconds=5) if now.hour % 2 else datetime(now.year, now.month, now.day, now.hour, 0, 0, 0).astimezone(pytz.timezone(config.TIMEZONE)) + timedelta(hours=1, minutes=1, seconds=5)

        try:
            s3_request = requests.get(f"{config.SPLATOON3_API}/schedules.json", headers=config.HEADERS_BASE, timeout = 10)
            self.__splatoon3_data = s3_request.json()["data"] if s3_request.status_code == 200 else None
        except requests.Timeout:
            self.__splatoon3_data = None

        try:
            s2_request = requests.get(f"{config.SPLATOON2_API}/schedules.json", headers=config.HEADERS_BASE, timeout = 10)
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
                await channel.send(f"<@&{config.ROTATION_ROLES_ID}>", embeds = embeds)


    @tasks.loop(seconds = 30)
    async def salmonrun_loop(self) -> None:
        now = datetime.now().astimezone(pytz.timezone(config.TIMEZONE))
        if (now - self.__salmon_start_time) < (self.__salmon_end_time - self.__salmon_start_time):
            return

        s3_request = requests.get(f"{config.SPLATOON3_API}/schedules.json", headers=config.HEADERS_BASE)
        if s3_request.status_code == 200:
            self.__salmonrun_data = s3_request.json()["data"]["coopGroupingSchedule"]

            self.__salmon_start_time = datetime.fromisoformat(self.__salmonrun_data["regularSchedules"]["nodes"][0]["startTime"][:-1]).astimezone(pytz.timezone(config.TIMEZONE)) + timedelta(hours = 1)
            self.__salmon_end_time   = datetime.fromisoformat(self.__salmonrun_data["regularSchedules"]["nodes"][0]["endTime"][:-1]).astimezone(pytz.timezone(config.TIMEZONE)) + timedelta(hours = 1, minutes = 1, seconds = 2)

            gears_request = requests.get(f"{config.SPLATOON3_API}/coop.json", headers=config.HEADERS_BASE)
            if gears_request.status_code == 200:
                self.__salmongears_data = gears_request.json()['data']['coopResult']['monthlyGear']
            else:
                self.__salmongears_data = None

            if not self.__started:
                return

            HDATA.check_splatoon3_data()

            with contextlib.suppress(Exception):
                channel = await self.__bot.fetch_channel(config.ROTATION_CHANNEL_ID)
                if channel is not None:
                    await channel.send(f"<@&{config.ROTATION_ROLES_ID}>", embed = RH.generate_salmonrun_embed(self.__salmonrun_data, self.__salmongears_data, title = "Une nouvelle rotation est disponible !", new_rotation = True))
        else:
            self.__salmonrun_data   = None
            self.__salmongears_data = None

            self.__salmon_start_time = datetime.now().astimezone(pytz.timezone(config.TIMEZONE))
            self.__salmon_end_time   = datetime.now().astimezone(pytz.timezone(config.TIMEZONE)) + timedelta(hours = 1)

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
        else:
            await inter.send(":x: Oups, une erreur est survenue !", ephemeral = True)
            return

        await inter.send(embed = embed)

def setup(self) -> None:
    if config.ROTATIONS_ENABLED:
        self.add_cog(RotationsModule(self))
        logs.info("Le module a bien été détécté et chargé", "[ROTATIONS]")
    else:
        logs.warning("Le module n'a pas été chargé car il est désactivé dans la configuration", "[ROTATIONS]")