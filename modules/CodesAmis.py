import disnake, qrcode, os, time
from disnake.ext import commands

from helper.codesamis import Database, CodeChecker
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
CODES = ["<:3ds:1036763036674961468> Nintendo 3DS", "<:NintendoSwitch:1036762589667020881> Nintendo Switch", "<:PokemonHome:1036760555106615427> Pokémon Home", "<:PokemonGo:1036761587698114583> Pokémon Go", "<:PokemonMaster:1036761429145030656> Pokémon Master", "<:PokemonShuffle:1036761953323974656> Pokémon Shuffle", "<:PokemonCafeMix:1036761505074524211> Pokémon Cafémix"]

WAITING_MESSAGE = "Traitement en cours..."

class CodesAmisModule(commands.Cog):
    def __init__(self, bot: commands.AutoShardedInteractionBot):
        self.__bot  = bot
        self.__db   = None
        self.__code = CodeChecker()

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        if not self.__db:
            self.__db = Database("databases/CodesAmis.db")
            await self.__db.create_if_not_exists()
        logs.success("Le module a été initié correctement", "[CODES-AMIS]")

    @commands.slash_command(name = "ca", description = "Permet de gérer facilement ses codes amis", dm_permission = False)
    async def _friend_code(self, inter: disnake.CommandInteraction):
        return
    
    @_friend_code.sub_command(name = "ajouter", description = "Permet d'ajouter ou de modifier un de ses codes amis")
    async def _add(
        self, 
        inter: disnake.CommandInteraction,
        code_type: str = commands.Param(name = "type", description = "Choisissez le type de code ami que vous souhaitez ajouter ou modifier", choices = CHOICES),
        code: str = commands.Param(name = "code-ami", description = "Entrez le code ami")
    ) -> None:
        await inter.send(WAITING_MESSAGE, ephemeral = True)
        await self.__db.create_user_if_not_exists(inter.author.id)

        if not self.__code.check(code_type, code):
            return await inter.edit_original_message(":x: Le code ami entré n'est pas valide.")
        
        await self.__db.change_friend_code(inter.author.id, code_type, self.__code.format(code_type, code))

        await inter.edit_original_response(":white_check_mark: Le code ami a été ajouté ou modifié avec succès.")

    @_friend_code.sub_command(name = "supprimer", description = "Permet de supprimer un de ses codes amis")
    async def _delete(
        self, 
        inter: disnake.CommandInteraction, 
        code_type: str = commands.Param(name = "type", description = "Choisissez le code que vous souhaitez supprimer", choices = CHOICES),
    ) -> None:
        await inter.send(WAITING_MESSAGE, ephemeral = True)
        await self.__db.create_user_if_not_exists(inter.author.id)

        if (await self.__db.get_friends_codes(inter.author.id))[TYPES.index(code_type)] == "0":
            return await inter.edit_original_response(":x: Vous ne pouvez pas supprimer ce code ami, car il n'existe pas dans la base de données.")

        await self.__db.delete_friend_code(inter.author.id, code_type)

        await inter.edit_original_response(":white_check_mark: Le code a bien été retiré de la base de données.")

    async def _show(self, inter: disnake.Interaction, member: disnake.Member) -> None:
        if member.bot:
            return await inter.send(":x: C'est si beau de voir quelqu'un vouloir devenir ami avec des robots, mais malheureusement, cet amour est impossible.", ephemeral = True)

        await inter.send(WAITING_MESSAGE)
        await self.__db.create_user_if_not_exists(member.id)

        friends_codes = await self.__db.get_friends_codes(member.id)
        description = "".join(
            f"▫️{CODES[i]}: `{friends_codes[i] if friends_codes[i] != '0' else 'Aucun'}`\n"
            for i in range(len(friends_codes))
        )

        await inter.edit_original_response(content = "", embed = disnake.Embed(
            title       = f"👥 Codes-amis de {member}",
            description = description,
            color       = 0xffffff
        ))

    @_friend_code.sub_command(name = "liste", description = "Permet de voir ses codes amis ou celui d'un autre utilisateur")
    async def _show_command(self, inter: disnake.CommandInteraction, member: disnake.Member = commands.Param(name = "membre", description = "Personne dont vous voulez voir les codes amis", default = lambda inter: inter.author)) -> None:
        await self._show(inter, member)

    @commands.user_command(name = "Afficher ses codes amis")
    async def _show_interaction(self, inter: disnake.UserCommandInteraction, member: disnake.Member) -> None:
        if not inter.guild:
            return await inter.send("Vous ne pouvez pas effectuer cette action ici.", ephemeral = True)

        await self._show(inter, member)

    @_friend_code.sub_command(name = "qrcode", description = "Permet d'obtenir un code ami sous forme de QR Code")
    async def show_qrcode_command(self, inter: disnake.CommandInteraction, code_type: str = commands.Param(name = "type", description = "Choisissez le type de code ami que vous souhaitez transformer en QR Code", choices = QRCODE_CHOICES),member: disnake.Member = commands.Param(name = "membre", description = "Personne dont vous voulez générer un QR Code pour un de ses codes amis", default = lambda inter: inter.author)):
        if member.bot:
            return await inter.send(":x: C'est si beau de voir quelqu'un vouloir devenir ami avec des robots, mais malheureusement, cet amour est impossible.", ephemeral = True)

        await inter.send(WAITING_MESSAGE)
        await self.__db.create_user_if_not_exists(member.id)

        friends_codes = await self.__db.get_friends_codes(inter.author.id)
        if friends_codes[TYPES.index(code_type)] == "0":
            return await inter.edit_original_response(":x: Vous ne pouvez pas générer un QR Code pour ce code ami, car il n'existe pas dans la base de données.")
        
        file_path = f"./tmp/qrcode-{member.id}-{int(time.time())}.png"
        qrcode.make(friends_codes[TYPES.index(code_type)]).save(file_path)

        await inter.edit_original_message(content = "", embed = disnake.Embed(
            title = "👥 Code ami",
            description = f"Scannez ce QR Code pour ajouter {member.mention} sur **{QRCODES_TYPE[code_type]}**",
            color = 0xffffff
        ).set_image(url = "attachment://qrcode.png"), file = disnake.File(file_path, filename = "qrcode.png"))

        os.remove(file_path)

def setup(self) -> None:
    self.add_cog(CodesAmisModule(self))
    logs.info("Le module a bien été détécté et chargé", "[CODES-AMIS]")