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
