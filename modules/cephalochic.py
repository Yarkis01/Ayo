from datetime import datetime, timedelta
import json
import time

from disnake.ext import commands, tasks
import disnake
import pytz

from utils.config import Config
from utils.embed import Embed
from utils.icons import get_ability_icon, get_brand_icon
from utils.logger import Logger
from utils.requests import make_api_request


class CephalochicModule(commands.Cog):
    def __init__(self, bot: commands.AutoShardedInteractionBot):
        self.__bot = bot
        self.__config: Config = bot.config

        self.__is_started = False
        self.__timezone = pytz.timezone(self.__config.timezone)

        self.__s3_data = None
        self.__s2_data = None

        self.__s3_next_rotation = self.__timezone.localize(datetime(1970, 1, 1))
        self.__s2_next_rotation = self.__timezone.localize(datetime(1970, 1, 1))

    def convert_to_timestamp(self, date_string: str) -> int:
        date = self.__timezone.localize(
            datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%SZ")
        )
        return int(date.timestamp()) + int(date.utcoffset().total_seconds())

    def generate_splatoon3_translation_string(
        self, gear: dict, translation: dict
    ) -> str:
        return translation["gear"].get(
            gear["gear"]["__splatoon3ink_id"], {"name": gear["gear"]["name"]}
        )["name"]

    def generate_splatoon3_abilities_string(self, gear: dict) -> str:
        abilities = get_ability_icon(gear["gear"]["primaryGearPower"]["name"])
        for ability in gear["gear"]["additionalGearPowers"]:
            abilities += get_ability_icon(ability["name"])

        return abilities

    def generate_splatoon2_abilities_string(self, gear: dict) -> str:
        abilities = get_ability_icon(gear["skill"]["name"])
        for _ in range(gear["gear"]["rarity"]):
            abilities += get_ability_icon("Unknown")

        return abilities

    def generate_splatoon2_translation_string(
        self, gear: dict, translation: dict
    ) -> str:
        if gear["gear"]["id"] in translation["gear"]:
            return translation["gear"][gear["gear"]["id"]]["name"]
        elif gear["gear"]["id"] in translation["gear"]["clothes"]:
            return translation["gear"]["clothes"][gear["gear"]["id"]]["name"]
        elif gear["gear"]["id"] in translation["gear"]["shoes"]:
            return translation["gear"]["shoes"][gear["gear"]["id"]]["name"]
        elif gear["gear"]["id"] in translation["gear"]["head"]:
            return translation["gear"]["head"][gear["gear"]["id"]]["name"]
        else:
            return gear["gear"]["name"]

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        if not self.__is_started:
            self._s3_update_loop.start()
            self._s2_update_loop.start()
            self.__is_started = True

        Logger.success("The module has been started correctly", "cephalochic")

    @tasks.loop(seconds=60)
    async def _s3_update_loop(self) -> None:
        if (
            self.__s3_next_rotation - self.__timezone.localize(datetime.utcnow())
        ) >= timedelta(hours=0):
            return

        data = await make_api_request(f"{self.__config.splatoon3_api}/gear.json")
        if not data:
            self.__s3_next_rotation = self.__timezone.localize(
                datetime.utcnow() + timedelta(hours=1)
            )
            return

        next_rotation = self.__timezone.localize(
            datetime.strptime(
                data["data"]["gesotown"]["limitedGears"][0]["saleEndTime"],
                "%Y-%m-%dT%H:%M:%SZ",
            )
        ) + timedelta(minutes=1, seconds=5)

        if next_rotation == self.__s3_next_rotation:
            self.__s3_next_rotation = self.__timezone.localize(
                datetime.utcnow() + timedelta(minutes=15)
            )
            return

        self.__s3_next_rotation = next_rotation
        self.__s3_data = data["data"]["gesotown"]

    @tasks.loop(seconds=60)
    async def _s2_update_loop(self) -> None:
        now = datetime.fromtimestamp(int(time.time())).astimezone(
            pytz.timezone(self.__config.timezone)
        )

        if (self.__s2_next_rotation - now) >= timedelta(hours=0):
            return

        data = await make_api_request(
            f"{self.__config.splatoon2_api}/merchandises.json"
        )
        if not data:
            self.__s2_next_rotation = self.__timezone.localize(
                datetime(now.year, now.month, now.day, now.hour, 0, 0, 0)
                + timedelta(hours=1)
            )
            return

        next_rotation = datetime.fromtimestamp(
            data["merchandises"][0]["end_time"]
        ).astimezone(pytz.timezone(self.__config.timezone)) + timedelta(
            minutes=1, seconds=5
        )

        if next_rotation == self.__s2_next_rotation:
            self.__s2_next_rotation = self.__timezone.localize(
                datetime(now.year, now.month, now.day, now.hour, 0, 0, 0)
                + timedelta(minutes=15)
            )
            return

        self.__s2_data = data["merchandises"]
        self.__s2_next_rotation = next_rotation

    @commands.slash_command(name="cephalochic", dm_permission=False)
    async def _cephalochic_command(self, inter: disnake.CommandInteraction) -> None:
        await inter.response.defer()

    @_cephalochic_command.sub_command(
        name="splatoon3",
        description="Permet d'avoir les équipements actuels de la boutique Céphalochic. (Splatoon 3)",
    )
    async def _cephalochic_s3_command(self, inter: disnake.CommandInteraction) -> None:
        if not self.__s3_data:
            await inter.send(
                embed=Embed.error(
                    title=":x: Oups une erreur est survenue !",
                    description="Veuillez réessayer dans quelques instants.\nSi le problème persiste, merci de bien vouloir contacter le support.",
                )
            )
            return

        translation = json.load(open("./data/s3/translation.json"))
        pickup_brand = self.__s3_data["pickupBrand"]["brand"]

        embed = Embed.splatoon3(
            title="<:cephalochic:1055073131808686091> Boutique Céphalochic",
            description=f"Voici les équipements actuels de la boutique Céphalochic.\nProchain chouchou du jour disponible <t:{self.convert_to_timestamp(self.__s3_data['pickupBrand']['saleEndTime'])}:R>",
        ).add_field(
            name=f"😍 Chouchou du jour - {get_brand_icon(pickup_brand['name'])} {translation['brands'][pickup_brand['id']]['name']}",
            value="\n".join(
                [
                    f"- {self.generate_splatoon3_translation_string(gear, translation)} (<:coins:1055085552510185502> {gear['price']}) - {self.generate_splatoon3_abilities_string(gear)}"
                    for gear in self.__s3_data["pickupBrand"]["brandGears"]
                ]
            ),
            inline=False,
        )

        for gear in self.__s3_data["limitedGears"]:
            embed.add_field(
                name=f"{get_brand_icon(gear['gear']['brand']['name'])} {self.generate_splatoon3_translation_string(gear, translation)}",
                value=f"- {self.generate_splatoon3_abilities_string(gear)}\n- <:coins:1055085552510185502> {gear['price']}\n<t:{self.convert_to_timestamp(gear['saleEndTime'])}:R>",
                inline=True,
            )

        await inter.send(
            embed=embed.set_image(url=self.__s3_data["pickupBrand"]["image"]["url"])
        )

    @_cephalochic_command.sub_command(
        name="splatoon2",
        description="Permet d'avoir les équipements actuels de la boutique Céphalochic. (Splatoon 2)",
    )
    async def _cephalochic_s2_command(self, inter: disnake.CommandInteraction) -> None:
        if not self.__s2_data:
            await inter.send(
                embed=Embed.error(
                    title=":x: Oups une erreur est survenue !",
                    description="Veuillez réessayer dans quelques instants.\nSi le problème persiste, merci de bien vouloir contacter le support.",
                )
            )
            return

        embed = Embed.splatoon2(
            title="<:cephalochic:1055073131808686091> Boutique Céphalochic",
            description=f"Voici les équipements actuels de la boutique Céphalochic.\nProchain équipement disponible <t:{self.__s2_data[0]['end_time']}:R>",
        )

        translation = json.load(open("./data/s2/translation.json"))
        for gear in self.__s2_data:
            embed.add_field(
                name=f"{get_brand_icon(gear['gear']['brand']['name'])} {self.generate_splatoon2_translation_string(gear, translation)}",
                value=f"- {self.generate_splatoon2_abilities_string(gear)}\n- <:coins:1055085552510185502> {gear['price']}\n<t:{gear['end_time']}:R>",
            )

        await inter.send(embed=embed)


def setup(self) -> None:
    self.add_cog(CephalochicModule(self))
