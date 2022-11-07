import disnake, qrcode, sqlite3, time, os, config
from disnake.ext import commands

import helper.codesamis as CA 
from utils.logger import logs

CHOICES = {
    "Nintendo 3DS (XXXX-XXXX-XXXX)": "ds",
    "Nintendo Switch (SW-XXXX-XXXX-XXXX)": "switch",
    "Pokémon Home (XXXXXXXXXXXX)": "home",
    "Pokémon GO (XXXX-XXXX-XXXX)": "pogo",
    "Pokémon Master (XXXX-XXXX-XXXX-XXXX)": "master",
    "Pokémon Shuffle (XXXXXXXX)": "shuffle",
    "Pokémon Cafemix (XXXX-XXXX-XXXX)": "cafemix"
}

QRCODE_CHOICES = {
    "Pokémon Home": "home",
    "Pokémon GO": "pogo"
}

QRCODES_TYPE = {
    "home": "Pokémon Home",
    "pogo": "Pokémon GO"
}

TYPES = ["ds", "switch", "home", "pogo", "master", "shuffle", "cafemix"]

class CodesAmisModule(commands.Cog):
    def __init__(self, bot: commands.AutoShardedInteractionBot) -> None:
        self.__bot = bot

        self.__db = sqlite3.connect("databases/CodesAmis.db")
        cursor = self.__db.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS "CA" ("id" TEXT, "ds" TEXT, "wiiu" TEXT, "switch" TEXT, "pogo" TEXT, "shuffle" TEXT, "master" TEXT, "home" TEXT, "cafemix" TEXT, PRIMARY KEY("id"));""")
        self.__db.commit()
        cursor.close()

    async def is_user_on_database(self, user_id: int) -> bool:
        cursor = self.__db.cursor()
        cursor.execute('''SELECT * FROM "CA" WHERE id = ?''', (user_id,))
        data = cursor.fetchone()
        cursor.close()
        return data is not None

    async def create_user_on_database(self, user_id: int) -> None:
        cursor = self.__db.cursor()
        cursor.execute('''INSERT INTO "CA" VALUES(?, "0", "0", "0", "0", "0", "0", "0", "0")''', (user_id,))
        self.__db.commit()
        cursor.close()

    async def get_friends_codes(self, user_id: int) -> tuple:
        cursor = self.__db.cursor()
        cursor.execute('''SELECT ds, switch, home, pogo, master, shuffle, cafemix FROM "CA" WHERE id = ?''', (user_id,))
        data = cursor.fetchone()
        cursor.close()
        return data

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        logs.success("Le module a été initié correctement", "[CODES-AMIS]")


    @commands.slash_command(name = "ca", description = "Permet de gérer facilement ses codes amis", dm_permission = False)
    async def ca_command(self, inter: disnake.CommandInteraction):
        return

    @ca_command.sub_command(name = "ajouter", description = "Permet d'ajouter ou de modifier un de ses codes amis")
    async def add_ca_command(
        self, 
        inter: disnake.CommandInteraction, 
        _type: str = commands.Param(name = "type", description = "Choisissez le type de code ami que vous souhaitez ajouter ou modifier", choices = CHOICES),
        code: str = commands.Param(name = "code-ami", description = "Entrez le code ami")
    ):
        await inter.send("Traitement en cours...", ephemeral = True)

        if _type == "ds" or _type == "pogo":
            valid = CA.check_ds_code(code)
            if not valid:
                return await inter.edit_original_response(":x: Erreur - Code ami non valide")
            code = CA.format_ds_code(code)
        elif _type == "switch":
            valid = CA.check_switch_code(code)
            if not valid:
                return await inter.edit_original_response(":x: Erreur - Code ami non valide")
            code = CA.format_switch_code(code)
        elif _type == "home":
            valid = CA.check_home_code(code)
            if not valid:
                return await inter.edit_original_response(":x: Erreur - Code ami non valide")
            code = CA.format_home_code(code)
        elif _type == "master":
            valid = CA.check_master_code(code)
            if not valid:
                return await inter.edit_original_response(":x: Erreur - Code ami non valide")
            code = CA.format_master_code(code)
        elif _type == "shuffle":
            valid = CA.check_shuffle_code(code)
            if not valid:
                return await inter.edit_original_response(":x: Erreur - Code ami non valide")
            code = CA.format_shuffle_code(code)
        elif _type == "cafemix":
            valid = CA.check_cafemix_code(code)
            if not valid:
                return await inter.edit_original_response(":x: Erreur - Code ami non valide")
            code = CA.format_cafemix_code(code)
        else:
            return await inter.edit_original_response(":x: Une erreur est survenue !")

        if not await self.is_user_on_database(inter.author.id):
            await self.create_user_on_database(inter.author.id)

        cursor = self.__db.cursor()
        cursor.execute(f'''UPDATE "CA" SET {_type} = ? WHERE id = ?''', (code, inter.author.id))
        self.__db.commit()
        cursor.close()

        await inter.edit_original_response("Le code ami a été ajouté ou modifié avec succès !")

    @ca_command.sub_command(name = "supprimer", description = "Permet de supprimer un de ses codes amis")
    async def delete_ca_command(
        self, 
        inter: disnake.CommandInteraction, 
        _type: str = commands.Param(name = "type", description = "Choisissez le code que vous souhaitez supprimer", choices = CHOICES),
    ):
        await inter.send("Traitement en cours...", ephemeral = True)

        if not await self.is_user_on_database(inter.author.id):
            await self.create_user_on_database(inter.author.id)

        data = await self.get_friends_codes(inter.author.id)

        if str(data[TYPES.index(_type)]) == "0":
            return await inter.edit_original_response("Vous ne pouvez pas supprimer ce code ami, car il n'existe pas dans la base de données.")

        cursor = self.__db.cursor()
        cursor.execute(f'''UPDATE "CA" SET {_type} = ? WHERE id = ?''', ("0", inter.author.id))
        self.__db.commit()
        cursor.close()

        await inter.edit_original_response("Le code a bien été retiré de la base de données.")

    async def show_friend_code(self, inter, member) -> None:
        if member.bot:
            return await inter.send(":x: Vous ne pouvez pas voir les codes amis d'un bot", ephemeral = True)

        await inter.send("Chargement...")

        if not await self.is_user_on_database(member.id):
            await self.create_user_on_database(member.id)

        data = await self.get_friends_codes(member.id)

        await inter.edit_original_message(content = "", embed = disnake.Embed(
            title = f"👥 Codes-amis de {member}",
            description = f"""▫️<:3ds:1036763036674961468> Nintendo 3DS: `{'Aucun' if str(data[0]) == '0' else str(data[0])}`
▫️<:NintendoSwitch:1036762589667020881> Nintendo Switch: `{'Aucun' if str(data[1]) == '0' else str(data[1])}`
▫️<:PokemonHome:1036760555106615427> Pokémon Home: `{'Aucun' if str(data[2]) == '0' else str(data[2])}`
▫️<:PokemonGo:1036761587698114583> Pokémon Go: `{'Aucun' if str(data[3]) == '0' else str(data[3])}`
▫️<:PokemonMaster:1036761429145030656> Pokémon Master: `{'Aucun' if str(data[4]) == '0' else str(data[4])}`
▫️<:PokemonShuffle:1036761953323974656> Pokémon Shuffle: `{'Aucun' if str(data[5]) == '0' else str(data[5])}`
▫️<:PokemonCafeMix:1036761505074524211> Pokémon Cafémix: `{'Aucun' if str(data[6]) == '0' else str(data[6])}`
""",
            color = 0xffffff
        ))

    @ca_command.sub_command(name = "liste", description = "Permet de voir ses codes amis ou celui d'un autre utilisateur")
    async def show_ca_command(self, inter: disnake.CommandInteraction, member: disnake.Member = commands.Param(name = "membre", description = "Personne dont vous voulez voir les codes amis", default = lambda inter: inter.author)):
        await self.show_friend_code(inter, member)

    @commands.user_command(name = "Afficher ses codes amis")
    async def liquider_user_command(self, inter: disnake.UserCommandInteraction, member: disnake.Member) -> None:
        await self.show_friend_code(inter, member)

    @ca_command.sub_command(name = "qrcode", description = "Permet d'obtenir un code ami sous forme de QR Code")
    async def show_qrcode_command(self, inter: disnake.CommandInteraction, _type: str = commands.Param(name = "type", description = "Choisissez le type de code ami que vous souhaitez transformer en QR Code", choices = QRCODE_CHOICES),member: disnake.Member = commands.Param(name = "membre", description = "Personne dont vous voulez générer un QR Code pour un de ses codes amis", default = lambda inter: inter.author)):
        if member.bot:
            return await inter.send(":x: Vous ne pouvez pas voir les codes amis d'un bot", ephemeral = True)

        await inter.send("Chargement...", ephemeral = False)

        if not await self.is_user_on_database(member.id):
            await self.create_user_on_database(member.id)

        data = await self.get_friends_codes(member.id)

        if str(data[TYPES.index(_type)]) == "0":
            return await inter.edit_original_response(":x: Vous ne pouvez pas générer un QR Code pour ce code ami, car il n'existe pas dans la base de données.")

        file_path = f"./tmp/qrcode-{member.id}-{int(time.time())}.png"
        image = qrcode.make(str(data[TYPES.index(_type)]))
        image.save(file_path)

        await inter.edit_original_message(content = "", embed = disnake.Embed(
            title = "👥 Code ami",
            description = f"Scannez ce QR Code pour ajouter {member.mention} sur **{QRCODES_TYPE[_type]}**",
            color = 0xffffff
        ).set_image(url = "attachment://qrcode.png"), file = disnake.File(file_path, filename = "qrcode.png"))

        os.remove(file_path)


def setup(self) -> None:
    if config.CODESAMIS_ENABLED:
        self.add_cog(CodesAmisModule(self))
        logs.info("Le module a bien été détécté et chargé", "[CODES-AMIS]")
    else:
        logs.warning("Le module n'a pas été chargé car il est désactivé dans la configuration", "[CODES-AMIS]")