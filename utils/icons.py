def get_rule_icon(mode: str) -> str:
    match mode:
        case "Expédition risquée":
            return "<:ExpeditionRisque:1036691276017455196>"
        case "Mission Bazookarpe":
            return "<:MissionBazookarpe:1036691565688668190>"
        case "Défense de zone":
            return "<:DefenseDeZone:1036691255125606400>"
        case "Pluie de palourdes":
            return "<:PluieDePalourdes:1036691257629618307>"
        case _:
            return "<:Classique:1036691264504078336>"

def get_friend_code_icon(code_type: str) -> str:
    match code_type:
        case "ds":
            return "<:3ds:1036763036674961468>"
        case "switch":
            return "<:NintendoSwitch:1036762589667020881>"
        case "home":
            return "<:PokemonHome:1036760555106615427>"
        case "shuffle":
            return "<:PokemonShuffle:1036761953323974656>"
        case "master":
            return "<:PokemonMaster:1036761429145030656>"
        case "cafemix":
            return "<:PokemonCafeMix:1036761505074524211>"
        case "pogo":
            return "<:PokemonGo:1036761587698114583>"
        case _:
            return "❓"