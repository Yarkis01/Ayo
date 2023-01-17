import disnake, config, pytz, requests, asyncio, json
from disnake.ext import commands, tasks
from datetime import datetime, timedelta

import helper.data as HDATA
from helper.icons import get_brand_icon, get_ability_icon
from utils.logger import logs

def splatoon3_generate_gear_line(gear: dict, translation: dict, brand: bool = False) -> str:
    abilities = get_ability_icon(gear["gear"]["primaryGearPower"]["name"])
    for ability in gear["gear"]["additionalGearPowers"]:
        abilities += get_ability_icon(ability["name"])

    brand_icon = f"{get_brand_icon(gear['gear']['brand']['name'])} " if brand else ""

    return f"{'' if brand else '- '}{brand_icon}{translation['gear'][gear['gear']['__splatoon3ink_id']]['name']} (<:coins:1055085552510185502> {gear['price']}) - {abilities}\n"

def splatoon2_generate_gear_line(gear: dict, translation: dict) -> str:
    abilities = get_ability_icon(gear["skill"]["name"])
    for _ in range(gear["gear"]["rarity"]):
        abilities += get_ability_icon("Unknown")
        
    if gear["gear"]["id"] in translation["gear"]:
        name = translation["gear"][gear["gear"]["id"]]["name"]
    elif gear["gear"]["id"] in translation["gear"]["clothes"]:
        name = translation["gear"]["clothes"][gear["gear"]["id"]]["name"]
    elif gear["gear"]["id"] in translation["gear"]["shoes"]:
        name = translation["gear"]["shoes"][gear["gear"]["id"]]["name"]
    elif gear["gear"]["id"] in translation["gear"]["head"]:
        name = translation["gear"]["head"][gear["gear"]["id"]]["name"]
    else:
        name = gear["gear"]["name"]

    return f"- {get_brand_icon(gear['gear']['brand']['name'])} {name} (<:coins:1055085552510185502> {gear['price']}) - {abilities}\n"

class CephalochicModule(commands.Cog):
    def __init__(self, bot: commands.AutoShardedInteractionBot) -> None:
        self.__bot = bot

        self.__s2_cephalochic_data = None
        self.__s3_cephalochic_data = None

        self.__s2_cephalochic_next_rotation = datetime(2022, 10, 30, 22, 0, 0, 0).astimezone(pytz.timezone(config.TIMEZONE))
        self.__s3_cephalochic_next_rotation = datetime(2022, 10, 30, 22, 0, 0, 0).astimezone(pytz.timezone(config.TIMEZONE))

        self.__started = False

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        if not self.__started:
            self.splatoon2_cephalochic_loop.start()
            self.splatoon3_cephalochic_loop.start()
        logs.info("Le module est en train d'être initié", "[CEPHALOCHIC]")
        await asyncio.sleep(10)
        self.__started = True
        logs.success("Le module a été initié correctement", "[CEPHALOCHIC]")



    @tasks.loop(seconds = 30)
    async def splatoon2_cephalochic_loop(self) -> None:
        now = datetime.now().astimezone(pytz.timezone(config.TIMEZONE))
        if (self.__s2_cephalochic_next_rotation - now) >= timedelta(hours = 0):
            return

        try:
            request                    = requests.get(f"{config.SPLATOON2_API}/merchandises.json", headers = config.HEADERS_BASE, timeout = config.TIMEOUT)
            self.__s2_cephalochic_data = request.json()["merchandises"] if request.status_code == 200 else None
        except requests.Timeout:
            self.__s2_cephalochic_data = None

        if self.__s2_cephalochic_data is None:
            self.__s2_cephalochic_next_rotation = datetime(now.year, now.month, now.day, now.hour, 0, 0, 0).astimezone(pytz.timezone(config.TIMEZONE)) + timedelta(hours = 1)
        else:
            self.__s2_cephalochic_next_rotation = datetime.fromtimestamp(self.__s2_cephalochic_data[0]["end_time"]).astimezone(pytz.timezone(config.TIMEZONE)) + timedelta(minutes = 1, seconds = 2)



    @tasks.loop(seconds = 30)
    async def splatoon3_cephalochic_loop(self) -> None:
        now = datetime.now().astimezone(pytz.timezone(config.TIMEZONE))
        if (self.__s3_cephalochic_next_rotation - now) >= timedelta(hours = 0):
            return

        try:
            request                    = requests.get(f"{config.SPLATOON3_API}/gear.json", headers = config.HEADERS_BASE, timeout = config.TIMEOUT)
            self.__s3_cephalochic_data = request.json()["data"]["gesotown"] if request.status_code == 200 else None
        except requests.Timeout:
            self.__s3_cephalochic_data = None

        if self.__s3_cephalochic_data is None:
            self.__s3_cephalochic_next_rotation = datetime(now.year, now.month, now.day, now.hour, 0, 0, 0).astimezone(pytz.timezone(config.TIMEZONE)) + timedelta(hours = 1)
            return
        
        self.__s3_cephalochic_next_rotation = datetime.fromisoformat(self.__s3_cephalochic_data["limitedGears"][0]["saleEndTime"][:-1]).astimezone(pytz.timezone(config.TIMEZONE)) + timedelta(hours = config.ADD_HOURS, minutes = 1, seconds = 2)

        if self.__started:
            HDATA.check_splatoon3_data()



    @commands.slash_command(name = "cephalochic", description = "Permet de récupérer les équipements disponibles dans la boutique Céphalochic", dm_permission = False)
    async def _cephalochic(
        self, 
        inter: disnake.CommandInteraction, 
        choice = commands.Param(name = "jeu", description = "La boutique Céphalochic de quel jeu, voulez-vous ?", choices = {
            "Splatoon 3": "s3",
            "Splatoon 2": "s2"
        })
    ) -> None:
        if (choice == "s3" and self.__s3_cephalochic_data is None) or (choice == "s2" and self.__s2_cephalochic_data is None):
            await inter.send(embed = disnake.Embed(
                title       = "<:cephalochic:1055073131808686091> Boutique Céphalochic",
                description = "Une erreur est survenue, veuillez réessayer ultérieurement.",
                color       = disnake.Colour.red() 
            ), ephemeral = True)
            return

        translation = json.load(open("./data/splatoon3.json") if choice == "s3" else open("./data/splatoon2.json"))
        next_rotation = self.__s2_cephalochic_data[0]["end_time"] if choice == "s2" else datetime.timestamp(datetime.fromisoformat(self.__s3_cephalochic_data["limitedGears"][0]["saleEndTime"][:-1]).astimezone(pytz.timezone(config.TIMEZONE)) + timedelta(hours = 1)) 
        
        embed = disnake.Embed(
            title       = f"{'<:Splatoon3:1036691272871718963>' if choice == 's3' else '<:Splatoon2:1036691271076560936>'}<:cephalochic:1055073131808686091> Boutique Céphalochic",
            description = f"Voici les équipements actuels de la boutique Céphalochic.\nProchain équipement disponible <t:{int(next_rotation)}:R>.",
            color       = 0xebeb3f if choice == "s3" else 0xf03c78
        )

        if choice == "s3":
            embed.add_field(
                name   = f"😍 Chouchou du jour - {get_brand_icon(self.__s3_cephalochic_data['pickupBrand']['brand']['name'])} {translation['brands'][self.__s3_cephalochic_data['pickupBrand']['brand']['id']]['name']}",
                value  = "".join([splatoon3_generate_gear_line(gear, translation) for gear in self.__s3_cephalochic_data["pickupBrand"]["brandGears"]]),
                inline = False 
            ).set_image(
                url = self.__s3_cephalochic_data["pickupBrand"]["image"]["url"]
            ).set_footer(
                text = "Données provenant de l'API du site Splatoon3.ink", icon_url = "https://i.imgur.com/Ufv6yH4.png"
            )

            gears_embed = disnake.Embed(
                title = "👚 Équipement",
                description = "".join([splatoon3_generate_gear_line(gear, translation, brand = True) for gear in self.__s3_cephalochic_data["limitedGears"]]),
                color = 0xebeb3f
            ).set_footer(
                text = "Données provenant de l'API du site Splatoon3.ink", icon_url = "https://i.imgur.com/Ufv6yH4.png"
            )

            await inter.send(embeds = [embed, gears_embed])
        else:
            embed.add_field(
                name   = "👚 Équipement",
                value  = "".join([splatoon2_generate_gear_line(gear, translation) for gear in self.__s2_cephalochic_data]),
                inline = False
            ).set_footer(
                text = "Données provenant de l'API du site Splatoon2.ink", icon_url = "https://i.imgur.com/nvxf5TK.png"
            )

            await inter.send(embed = embed)

def setup(self) -> None:
    if config.CEPHALOCHIC_ENABLED:
        self.add_cog(CephalochicModule(self))
        logs.info("Le module a bien été détécté et chargé", "[CEPHALOCHIC]")
    else:
        logs.warning("Le module n'a pas été chargé car il est désactivé dans la configuration", "[CEPHALOCHIC]")