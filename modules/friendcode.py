from disnake.ext import commands
import disnake
import ast

from utils.database   import Collections, Database
from utils.embed      import Embed
from utils.friendcode import ensure_user_exists, format_key, CodeChecker
from utils.icons      import get_friend_code_icon
from utils.logger     import Logger

CHOICES = {
    "Nintendo 3DS (XXXX-XXXX-XXXX)": "ds",
    "Nintendo Switch (SW-XXXX-XXXX-XXXX)": "switch",
    "Pokémon Home (XXXXXXXXXXXX)": "home",
    "Pokémon GO (XXXX-XXXX-XXXX)": "pogo",
    "Pokémon Master (XXXX-XXXX-XXXX-XXXX)": "master",
    "Pokémon Shuffle (XXXXXXXX)": "shuffle",
    "Pokémon Cafemix (XXXX-XXXX-XXXX)": "cafemix"
}

class FriendCodeModule(commands.Cog):
    def __init__(self, bot: commands.AutoShardedInteractionBot):
        self.__bot          = bot
        self.__db: Database = bot.database
        self.__code_checker = CodeChecker()
        
    @commands.Cog.listener()
    async def on_ready(self) -> None:
        Logger.success("The module has been started correctly", "friendcode")


    @commands.slash_command(name = "ca", description = "", dm_permission = False)
    async def _ca_command(self, inter: disnake.CommandInteraction) -> None:
        await ensure_user_exists(self.__db, inter.author.id)


    @_ca_command.sub_command(name = "acces", description = "Permet de sélectionner l'accès aux codes de vos amis.")
    async def _public_access_command(
        self,
        inter: disnake.CommandInteraction,
        allow: str = commands.Param(name = "visibilite", description = "Choisissez la visibilité des codes de vos amis", choices = {
            "Publique": "True", 
            "Privée": "False"
        })) -> None:
            await inter.response.defer(ephemeral = True)
            
            allow = ast.literal_eval(allow)
            await self.__db.update_document(Collections.FRIEND_CODE, { "uid": inter.author.id }, { "publicAccess": allow})

            await inter.send(embed = Embed.success(
                title       = "👀 Changement de visibilité",
                description = f"Vos codes amis sont maintenant **{'publics' if allow else 'privés'}**."
            ))


    @_ca_command.sub_command(name = "ajouter", description = "Permet d'ajouter ou de modifier un de ses codes amis")
    async def _add_command(
        self, 
        inter: disnake.CommandInteraction,
        code_type: str = commands.Param(name = "type", description = "Choisissez le type de code ami que vous souhaitez ajouter ou modifier", choices = CHOICES),
        code: str = commands.Param(name = "code-ami", description = "Entrez le code ami")
    ) -> None:
        await inter.response.defer(ephemeral = True)
        
        if not self.__code_checker.check(code_type, code):
            await inter.send(embed = Embed.error(":x: Code ami invalide", "Le code ami que vous avez entré n'est pas valide."))
            return
        
        await self.__db.update_document(Collections.FRIEND_CODE, { "uid": inter.author.id }, { f"friendCode.{code_type}": self.__code_checker.format(code_type, code) })
        await inter.send(embed = Embed.success(":white_check_mark: Code ami ajouté", "Votre code ami a bien été ajouté."))


    @_ca_command.sub_command(name = "supprimer", description = "Permet de supprimer un de ses codes amis")
    async def _del_command(
        self,
        inter: disnake.CommandInteraction,
        code_type: str = commands.Param(name = "type", description = "Choisissez le code que vous souhaitez supprimer", choices = CHOICES),
    ) -> None:
        await inter.response.defer(ephemeral = True)

        await self.__db.update_document(Collections.FRIEND_CODE, { "uid": inter.author.id }, { f"friendCode.{code_type}": None })
        await inter.send(embed = Embed.success(":white_check_mark: Code ami supprimé", "Votre code ami a bien été supprimé."))


    @_ca_command.sub_command(name = "liste", description = "Permet de voir ses codes amis ou ceux d'un autre utilisateur")
    async def _show_command(self, inter: disnake.CommandInteraction, member: disnake.User = commands.Param(lambda inter: inter.author, name = "membre", description = "Utilisateur dont vous souhaitez voir les codes amis.")) -> None:
        await self.show_friend_code(inter, member)

    @commands.user_command(name = "Afficher Codes Amis", dm_permission = False)
    async def _show_user_command(self, inter: disnake.UserCommandInteraction, member: disnake.User) -> None:
        await self.show_friend_code(inter, member)

    async def show_friend_code(self, inter: disnake.Interaction, member: disnake.User) -> None:
        await inter.response.defer()

        if member.bot:
            await inter.send(embed = Embed.error(":x: Code Ami", "Vous ne pouvez pas afficher les codes amis d'un bot"))
            return

        await ensure_user_exists(self.__db, member.id)
        data = await self.__db.find_one(Collections.FRIEND_CODE, { "uid": member.id })

        if not data["publicAccess"] and inter.author.id != member.id:
            await inter.send(embed = Embed.error(":x: Accès refusé", "Vous ne pouvez pas voir les codes d'amis de cet utilisateur car il a décidé de ne pas les mettre à la disposition des autres utilisateurs.\n\nSi vous souhaitez voir les codes d'amis de cet utilisateur, demandez-lui d'exécuter la commande pour les afficher ou d'autorisez l'accès public à ses codes d'amis."))
            return

        await inter.send(
            embed=Embed.default(
                title       = f"👥 Codes amis de {member.name}",
                description = "\n".join(
                    [
                        f"- {get_friend_code_icon(key)} {format_key(key)}: {f'`{value}`' if value is not None else '`Non défini`'}"
                        for key, value in data["friendCode"].items()
                    ]
                )
            )
        )



def setup(self) -> None:
    self.add_cog(FriendCodeModule(self))