import disnake, json, pytz, config
from datetime import datetime, timedelta

def get_ranked_icon(mode: str) -> str:
    if mode == "Expédition risquée":
        return "<:ExpeditionRisque:1036691276017455196>"
    elif mode == "Mission Bazookarpe":
        return "<:MissionBazookarpe:1036691565688668190>"
    elif mode == "Défense de zone":
        return "<:DefenseDeZone:1036691255125606400>"
    else:
        return "<:PluieDePalourdes:1036691257629618307>"

def generate_default_splatoon3_embed(data: dict, number: int, title: str, translation: dict, startTime: datetime, endTime: datetime) -> disnake.Embed:
    return disnake.Embed(
        title       = f"<:Splatoon3:1036691272871718963> {title}",
        description = f"Début: <t:{int(datetime.timestamp(startTime))}:f>\nFin: <t:{int(datetime.timestamp(endTime))}:f>",
        color       = 0xebeb3f
    ).add_field(
        name = "<:Classique:1036691264504078336> Match Classique",
        value = f"- {translation['stages'][data['regularSchedules']['nodes'][number]['regularMatchSetting']['vsStages'][0]['id']]['name']}\n- {translation['stages'][data['regularSchedules']['nodes'][number]['regularMatchSetting']['vsStages'][1]['id']]['name']}",
        inline = False
    ).add_field(
        name = f"<:Anarchie:1036691259865190540>Match Anarchie (serie)  -  {get_ranked_icon(translation['rules'][data['bankaraSchedules']['nodes'][number]['bankaraMatchSettings'][0]['vsRule']['id']]['name'])} {translation['rules'][data['bankaraSchedules']['nodes'][number]['bankaraMatchSettings'][0]['vsRule']['id']]['name']}",
        value = f"- {translation['stages'][data['bankaraSchedules']['nodes'][number]['bankaraMatchSettings'][0]['vsStages'][0]['id']]['name']}\n- {translation['stages'][data['bankaraSchedules']['nodes'][number]['bankaraMatchSettings'][0]['vsStages'][1]['id']]['name']}",
        inline = False
    ).add_field(
        name = f"<:Anarchie:1036691259865190540> Match Anarchie (ouvert)  -  {get_ranked_icon(translation['rules'][data['bankaraSchedules']['nodes'][number]['bankaraMatchSettings'][1]['vsRule']['id']]['name'])} {translation['rules'][data['bankaraSchedules']['nodes'][number]['bankaraMatchSettings'][1]['vsRule']['id']]['name']}",
        value = f"- {translation['stages'][data['bankaraSchedules']['nodes'][number]['bankaraMatchSettings'][1]['vsStages'][0]['id']]['name']}\n- {translation['stages'][data['bankaraSchedules']['nodes'][number]['bankaraMatchSettings'][1]['vsStages'][1]['id']]['name']}",
        inline = False
    ).set_footer(text = "Données provenant de l'API du site Splatoon3.ink", icon_url = "https://i.imgur.com/Ufv6yH4.png")

def generate_splatfest_splatoon3_embed(data: dict, number: int, title: str, translation: dict, startTime: datetime, endTime: datetime) -> disnake.Embed:
    return disnake.Embed(
        title       = f"<:Splatoon3:1036691272871718963><:splatfest:1040780648341848115> {title}",
        description = f"Début: <t:{int(datetime.timestamp(startTime))}:f>\nFin: <t:{int(datetime.timestamp(endTime))}:f>",
        color       = 0xebeb3f
    ).add_field(
        name   = "<:splatfest:1040780648341848115> Festimatch",
        value  = f"- {translation['stages'][data['festSchedules']['nodes'][number]['festMatchSetting']['vsStages'][0]['id']]['name']}\n- {translation['stages'][data['festSchedules']['nodes'][number]['festMatchSetting']['vsStages'][1]['id']]['name']}",
        inline = False
    ).add_field(
        name   = "<:splatfest:1040780648341848115> Match tricolore",
        value  = f"- {translation['stages'][data['currentFest']['tricolorStage']['id']]['name']}",
        inline = False
    ).set_image(
        url = data['currentFest']['tricolorStage']['image']['url']
    ).set_thumbnail(
        url = "https://i.imgur.com/DbKsMyr.png"
    ).set_footer(
        text = "Données provenant de l'API du site Splatoon3.ink", 
        icon_url = "https://i.imgur.com/Ufv6yH4.png"
    )

def generate_splatoon3_embed(data: dict, number: int = 0, title: str = "Rotation actuelle") -> disnake.Embed:
    translation = json.load(open("./data/splatoon3.json"))
    startTime   = datetime.fromisoformat(data["regularSchedules"]["nodes"][number]["startTime"][:-1]).astimezone(pytz.timezone(config.TIMEZONE)) + timedelta(hours = 1)
    endTime     = datetime.fromisoformat(data["regularSchedules"]["nodes"][number]["endTime"][:-1]).astimezone(pytz.timezone(config.TIMEZONE)) + timedelta(hours = 1)
    
    if data['regularSchedules']['nodes'][number]['regularMatchSetting'] is None:
        return generate_splatfest_splatoon3_embed(
            data, number, title, translation, startTime, endTime
        )
    else:
        return generate_default_splatoon3_embed(
            data, number, title, translation, startTime, endTime
        )

def generate_splatoon2_embed(data: dict, number: int = 0, title: str = "Rotation actuelle") -> disnake.Embed:
    translation = json.load(open("./data/splatoon2.json"))

    match_pro   = translation["rules"][data['gachi'][number]["rule"]["key"]]["name"]
    match_ligue = translation["rules"][data['league'][number]["rule"]["key"]]["name"]

    return disnake.Embed(
        title = f"<:Splatoon2:1036691271076560936> {title}",
        description = f"Début: <t:{data['regular'][number]['start_time']}:f>\nFin: <t:{data['regular'][number]['end_time']}:f>",
        color = 0xf03c78
    ).add_field(
        name = "<:Classique:1036691264504078336>Match Classique",
        value = f"- {translation['stages'][data['regular'][number]['stage_a']['id']]['name']}\n- {translation['stages'][data['regular'][number]['stage_b']['id']]['name']}",
        inline = False
    ).add_field(
        name = f"<:Anarchie:1036691259865190540> Match Pro  -  {get_ranked_icon(match_pro)} {match_pro}",
        value = f"- {translation['stages'][data['gachi'][number]['stage_a']['id']]['name']}\n- {translation['stages'][data['gachi'][number]['stage_b']['id']]['name']}",
        inline = False
    ).add_field(
        name = f"<:Ligue:1036691261844885626> Match de ligue  -  {get_ranked_icon(match_ligue)} {match_ligue}",
        value = f"- {translation['stages'][data['league'][number]['stage_a']['id']]['name']}\n- {translation['stages'][data['league'][number]['stage_b']['id']]['name']}",
        inline = False
    ).set_footer(text = "Données provenant de l'API du site Splatoon2.ink", icon_url = "https://i.imgur.com/nvxf5TK.png")

def generate_salmonrun_embed(data: dict, gear_data: dict, number: int = 0, title: str = "Rotation actuelle") -> disnake.Embed:
    data = data["regularSchedules"]["nodes"][number]
    translation = json.load(open("./data/splatoon3.json"))

    startTime = datetime.fromisoformat(data["startTime"][:-1]).astimezone(pytz.timezone(config.TIMEZONE)) + timedelta(hours = 1)
    endTime   = datetime.fromisoformat(data["endTime"][:-1]).astimezone(pytz.timezone(config.TIMEZONE)) + timedelta(hours = 1, seconds = 30)

    embed = disnake.Embed(
        title = f"<:Splatoon3:1036691272871718963><:SalmonRun:1036691274415231006> {title}",
        description = f"Début: <t:{int(datetime.timestamp(startTime))}:f>\nFin: <t:{int(datetime.timestamp(endTime))}:f>",
        color = 0xff5033
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
    ).set_footer(text = "Données provenant de l'API du site Splatoon3.ink", icon_url = "https://i.imgur.com/Ufv6yH4.png")

    if gear_data is not None:
        embed.set_thumbnail(gear_data["image"]["url"])
        try:
            embed.add_field(
                name   = "👚 Équipement actuel",
                value  = f"- {translation['gear'][gear_data['__splatoon3ink_id']]['name']}",
                inline = False
            )
        except:
            pass

    return embed