from datetime import datetime, timedelta
import json
import disnake
import pytz

from utils.icons import get_rule_icon

class Embed:
    """A class for creating different embed types."""
    
    @staticmethod    
    def make_embed(color, title, description):
        """Create an embed with the given color and info.
        
        Args: 
            color (int): Embed color in hexadecimal.
            title (str): Embed title.
            description (str): Embed description.
        
        Returns:
            disnake.Embed: The created embed.
        """
        return disnake.Embed(
            title=title,
            description=description,     
            color=color
        ).set_footer(
            text = "Réalisé avec ❤️ par Yarkis01",     
            icon_url = "https://avatars.githubusercontent.com/u/109750019?v=4"  
        )
            
    @staticmethod       
    def default(title: str, description: str) -> disnake.Embed:      
        """Create a default embed with white color."""       
        return Embed.make_embed(0xffffff, title, description)
        
    @staticmethod       
    def error(title: str, description: str) -> disnake.Embed:
        """Create an error embed with red color."""
        return Embed.make_embed(0xe74c3c, title, description)
        
    @staticmethod       
    def success(title: str, description: str) -> disnake.Embed:   
        """Create a success embed with green color."""    
        return Embed.make_embed(0x2ecc71, title, description)
    
    @staticmethod       
    def warning(title: str, description: str) -> disnake.Embed:   
        """Create a warning embed with yellow color."""   
        return Embed.make_embed(0xf1c40f, title, description)
    
    @staticmethod
    def splatoon2(title: str, description: str, color: int = 0xf03c78) -> disnake.Embed:
        """Create a Splatoon 2 embed"""
        return Embed.make_embed(color, f"<:Splatoon2:1036691271076560936> {title}", description).set_footer(text = "Données provenant de l'API du site Splatoon2.ink", icon_url = "https://i.imgur.com/nvxf5TK.png")
    
    @staticmethod
    def splatoon3(title: str, description: str, color: int = 0xebeb3f) -> disnake.Embed:
        """Create a Splatoon 3 embed"""
        return Embed.make_embed(color, f"<:Splatoon3:1036691272871718963> {title}", description).set_footer(text = "Données provenant de l'API du site Splatoon3.ink", icon_url = "https://i.imgur.com/Ufv6yH4.png")
    

class RotationsEmbed:
    def __init__(self, timezone: str):
        self.__timezone = pytz.timezone(timezone)
        
    def __convert_to_timestamp(self, date_string: str) -> int:
        date = self.__timezone.localize(datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%SZ"))
        return int(date.timestamp()) + int(date.utcoffset().total_seconds())
        
    def get_splatoon2_embed(self, data: dict, number: int = 0, title: str = "Rotation actuelle") -> disnake.Embed:
        translation = json.load(open("./data/s2/translation.json"))
        
        match_pro   = translation["rules"][data['gachi'][number]["rule"]["key"]]["name"]
        match_ligue = translation["rules"][data['league'][number]["rule"]["key"]]["name"]
        
        return Embed.splatoon2(
            title       = title,
            description = f"Début: <t:{data['regular'][number]['start_time']}:f>\nFin: <t:{data['regular'][number]['end_time']}:f>"
        ).add_field(
            name   = "<:classique:1137415472929853440> Match Classique",
            value  = f"- {translation['stages'][data['regular'][number]['stage_a']['id']]['name']}\n- {translation['stages'][data['regular'][number]['stage_b']['id']]['name']}",
            inline = False
        ).add_field(
            name   = f"<:anarchie:1137415471130476565> Match Pro - {get_rule_icon(match_pro)} {match_pro}",
            value  = f"- {translation['stages'][data['gachi'][number]['stage_a']['id']]['name']}\n- {translation['stages'][data['gachi'][number]['stage_b']['id']]['name']}",
            inline = False
        ).add_field(
            name   = f"<:ligue:1137415468047671427> Match de ligue - {get_rule_icon(match_ligue)} {match_ligue}",
            value  = f"- {translation['stages'][data['league'][number]['stage_a']['id']]['name']}\n- {translation['stages'][data['league'][number]['stage_b']['id']]['name']}",
            inline = False
        )
        
    def get_splatoon3_embed(self, data: dict, number: int = 0, title: str = "Rotation actuelle") -> disnake.Embed:
        translation = json.load(open("./data/s3/translation.json"))

        embed = Embed.splatoon3(
            title       = f"{title}",
            description = f"Début <t:{self.__convert_to_timestamp(data['regularSchedules']['nodes'][number]['startTime'])}:f>\nFin: <t:{self.__convert_to_timestamp(data['regularSchedules']['nodes'][number]['endTime'])}:f>"
        )

        if data['regularSchedules']['nodes'][number]['regularMatchSetting'] is None:
            embed.title = f"<:splatfest:1040780648341848115> {title}"
            embed.add_field(
                name="<:splatfest:1040780648341848115> Festimatch (Défi)",
                value=f"- {translation['stages'][data['festSchedules']['nodes'][number]['festMatchSettings'][0]['vsStages'][0]['id']]['name']}\n- {translation['stages'][data['festSchedules']['nodes'][number]['festMatchSettings'][0]['vsStages'][1]['id']]['name']}",
                inline=False
            )
            embed.add_field(
                name="<:splatfest:1040780648341848115> Festimatch (Ouvert)",
                value=f"- {translation['stages'][data['festSchedules']['nodes'][number]['festMatchSettings'][1]['vsStages'][0]['id']]['name']}\n- {translation['stages'][data['festSchedules']['nodes'][number]['festMatchSettings'][1]['vsStages'][1]['id']]['name']}",
                inline=False
            )
            embed.add_field(
                name="<:splatfest:1040780648341848115> Match tricolore",
                value="- Aléatoire" if str(data['currentFest']['tricolorStage']['name']).lower() == "random" else f"- {translation['stages'][data['currentFest']['tricolorStage']['id']]['name']}",
                inline=False,
            )
            embed.set_image(url=data['currentFest']['tricolorStage']['image']['url'])
            embed.set_thumbnail(url="https://i.imgur.com/DbKsMyr.png")
        else:
            embed.add_field(
                name="<:classique:1137415472929853440> Match Classique",
                value=f"- {translation['stages'][data['regularSchedules']['nodes'][number]['regularMatchSetting']['vsStages'][0]['id']]['name']}\n- {translation['stages'][data['regularSchedules']['nodes'][number]['regularMatchSetting']['vsStages'][1]['id']]['name']}",
                inline=False
            )
            embed.add_field(
                name=f"<:anarchie:1137415471130476565> Match Anarchie (serie)  -  {get_rule_icon(translation['rules'][data['bankaraSchedules']['nodes'][number]['bankaraMatchSettings'][0]['vsRule']['id']]['name'])} {translation['rules'][data['bankaraSchedules']['nodes'][number]['bankaraMatchSettings'][0]['vsRule']['id']]['name']}",
                value=f"- {translation['stages'][data['bankaraSchedules']['nodes'][number]['bankaraMatchSettings'][0]['vsStages'][0]['id']]['name']}\n- {translation['stages'][data['bankaraSchedules']['nodes'][number]['bankaraMatchSettings'][0]['vsStages'][1]['id']]['name']}",
                inline=False
            )
            embed.add_field(
                name=f"<:anarchie:1137415471130476565> Match Anarchie (ouvert)  -  {get_rule_icon(translation['rules'][data['bankaraSchedules']['nodes'][number]['bankaraMatchSettings'][1]['vsRule']['id']]['name'])} {translation['rules'][data['bankaraSchedules']['nodes'][number]['bankaraMatchSettings'][1]['vsRule']['id']]['name']}",
                value=f"- {translation['stages'][data['bankaraSchedules']['nodes'][number]['bankaraMatchSettings'][1]['vsStages'][0]['id']]['name']}\n- {translation['stages'][data['bankaraSchedules']['nodes'][number]['bankaraMatchSettings'][1]['vsStages'][1]['id']]['name']}",
                inline=False
            )
            embed.add_field(
                name=f"<:rangx:1048249026413342750> Match X - {get_rule_icon(translation['rules'][data['xSchedules']['nodes'][number]['xMatchSetting']['vsRule']['id']]['name'])} {translation['rules'][data['xSchedules']['nodes'][number]['xMatchSetting']['vsRule']['id']]['name']}",
                value=f"- {translation['stages'][data['xSchedules']['nodes'][number]['xMatchSetting']['vsStages'][0]['id']]['name']}\n- {translation['stages'][data['xSchedules']['nodes'][number]['xMatchSetting']['vsStages'][1]['id']]['name']}",
                inline=False
            )
        
        return embed
    
    def get_splatoon2_salmon_embed(self, data: dict, number: int = 0, title: str = "Rotation actuelle") -> disnake.Embed:
        if number == 2:
            return Embed.splatoon2(
                title       = f"<:SalmonRun:1036691274415231006> {title}",
                description = f"Début: <t:{data['schedules'][number]['start_time']}:f>\nFin: <t:{data['schedules'][number]['end_time']}:f>",
                color       = 0xff5033
            )
        
        translation = json.load(open("./data/s2/translation.json"))
        
        details = data["details"][number]
        weapons = [translation["weapons"].get(weapon['id'], {}).get("name", "Aléatoire") for weapon in details["weapons"]]
        
        return Embed.splatoon2(
            title       = f"<:SalmonRun:1036691274415231006> {title}",
            description = f"Début: <t:{details['start_time']}:f>\nFin: <t:{details['end_time']}:f>",
            color       = 0xff5033
        ).add_field(
            name="🗺️ Map",
            value=f"- {translation['coop_stages'][details['stage']['image']]['name']}",
            inline=False
        ).add_field(
            name="🔫 Armes",
            value=f"- {weapons[0]}\n- {weapons[1]}\n- {weapons[2]}\n- {weapons[3]}",
            inline=False
        ).set_image(
            url=f"https://splatoon2.ink/assets/splatnet{details['stage']['image']}"
        )
        
    def get_splatoon3_salmon_embed(self, data: dict, gear_data: dict, number: int = 0, title: str = "Rotation actuelle") -> disnake.Embed:
        regular_schedules = data["regularSchedules"]["nodes"]
        big_run_schedules = data["bigRunSchedules"]["nodes"]

        now        = datetime.now(self.__timezone) if number == 0 else self.__timezone.localize(datetime.strptime(regular_schedules[number]["endTime"], "%Y-%m-%dT%H:%M:%SZ"))
        start_time = self.__timezone.localize(datetime.strptime(regular_schedules[number + 1]["startTime"], "%Y-%m-%dT%H:%M:%SZ"))

        if (now - start_time) >= timedelta(hours=0) or not big_run_schedules:
            return self.__generate_splatoon3_salmon_embed(regular_schedules[number], gear_data, f"<:SalmonRun:1036691274415231006> {title}")

        title = "<:bigrun:1050787966794080379> Un Big Run fait des vagues !" if title == "Une nouvelle rotation est disponible !" else f"<:bigrun:1050787966794080379> {title}"
        return self.__generate_splatoon3_salmon_embed(big_run_schedules[0], gear_data, title)
    
    def __generate_splatoon3_salmon_embed(self, data: dict, gear_data: dict, title: str) -> disnake.Embed:
        translation = json.load(open("./data/s3/translation.json"))
        
        embed = Embed.splatoon3(
            title       = f"{title}",
            description = f"Début <t:{self.__convert_to_timestamp(data['startTime'])}:f>\nFin: <t:{self.__convert_to_timestamp(data['endTime'])}:f>",
            color       = 0xff5033
        ).set_image(
            data["setting"]["coopStage"]["image"]["url"]
        ).add_field(
            name   = "🗺️ Map",
            value  = f"- {translation['stages'][data['setting']['coopStage']['id']]['name']}",
            inline = False
        ).add_field(
            name   = "🔫 Armes",
            value  = f"- {translation['weapons'][data['setting']['weapons'][0]['__splatoon3ink_id']]['name']}\n- {translation['weapons'][data['setting']['weapons'][1]['__splatoon3ink_id']]['name']}\n- {translation['weapons'][data['setting']['weapons'][2]['__splatoon3ink_id']]['name']}\n- {translation['weapons'][data['setting']['weapons'][3]['__splatoon3ink_id']]['name']}",
            inline = False
        )
        
        if gear_data:
            embed.set_thumbnail(gear_data["image"]["url"])
            embed.add_field(
                name   = "👚 Équipement actuel",
                value  = f"- {translation['gear'][gear_data['__splatoon3ink_id']]['name']}",
                inline = False
            )
        
        return embed
    
    def __generate_no_defi_oeuf_sup_embed(self) -> disnake.Embed:
        return Embed.splatoon3(
            title       = "<:SalmonRun:1036691274415231006> Défi œuf sup'",
            description = "Aucune rotation n'est actuellement disponible dans ce mode de jeu.",
            color       = 0xFF5033
        )
    
    def get_defi_oeuf_sup_embed(self, data: dict, number: int = 0) -> disnake.Embed:
        if len(data["teamContestSchedules"]["nodes"]) == 0:
            return self.__generate_no_defi_oeuf_sup_embed()
        
        translation = json.load(open("./data/s3/translation.json"))
        data        = data["teamContestSchedules"]["nodes"][0]
        
        start_time = self.__timezone.localize(datetime.strptime(data["startTime"], "%Y-%m-%dT%H:%M:%SZ"))
        now        = self.__timezone.localize(datetime.utcnow()) if number == 0 else start_time
        
        if (now - start_time) >= timedelta(hours = 0):
            return Embed.splatoon3(
                title       = "<:Splatoon3:1036691272871718963><:SalmonRun:1036691274415231006> Défi œuf sup'",
                description = f"Début: <t:{self.__convert_to_timestamp(data['startTime'])}:f>\nFin: <t:{data['endTime']}:f>",
                color       = 0xFF5033,
            ).add_field(
                name   = "🗺️ Map",
                value  = f"- {translation['stages'][data['setting']['coopStage']['id']]['name']}",
                inline = False
            ).add_field(
                name   = "🔫 Armes",
                value  = "\n".join([f"- {translation['weapons'][weapon['__splatoon3ink_id']]['name']}" for weapon in data["setting"]["weapons"]]),
                inline = False
            ).set_image(
                data["setting"]["coopStage"]["image"]["url"]
            )
            
        return self.__generate_no_defi_oeuf_sup_embed()
    
    def get_event_schedules_embed(self, data: dict, number: int = 0) -> disnake.Embed:
        event_schedules = data.get("nodes", [])
        if len(event_schedules) < 2 or len(event_schedules[number].get("timePeriods", [])) == 0:
            return Embed.splatoon3(
                "<:challenge:1137693377597558804> Match Challenge",
                "Aucune rotation n'est actuellement disponible dans ce mode de jeu.",
                0xf02d7d
            )
            
        translation = json.load(open("./data/s3/translation.json"))
        data        = data["nodes"][number]
        
        leagueMatchSetting = data['leagueMatchSetting']
        leagueMatchEvent   = data['leagueMatchSetting']['leagueMatchEvent']
        
        embed = Embed.splatoon3(
            title       = f"{translation['events'][leagueMatchEvent['id']]['name']}\n<:challenge:1137693377597558804> {translation['events'][leagueMatchEvent['id']]['desc']}",
            description = str(translation['events'][leagueMatchEvent['id']]['regulation']).replace('<br />', '\n').replace('・', '- '),
            color       = 0xf02d7d
        ).add_field(
            name   = f"**{get_rule_icon(translation['rules'][leagueMatchSetting['vsRule']['id']]['name'])} {translation['rules'][leagueMatchSetting['vsRule']['id']]['name']}**",
            value  = f"- {translation['stages'][leagueMatchSetting['vsStages'][0]['id']]['name']}\n- {translation['stages'][leagueMatchSetting['vsStages'][1]['id']]['name']}",
            inline = False
        )
        
        for period in data['timePeriods']:
            embed.add_field(
                name   = "**📅 Créneau suivant**" if period == data['timePeriods'][0] else "<:invisible:1137708029417099274>",
                value  = f"Début <t:{self.__convert_to_timestamp(period['startTime'])}:f>\nFin: <t:{self.__convert_to_timestamp(period['endTime'])}:f>",
                inline = True
            )
            
        return embed