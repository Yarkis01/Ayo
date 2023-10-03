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
            return "<:classique:1137415472929853440>"


def get_friend_code_icon(code_type: str) -> str:
    match code_type:
        case "ds":
            return "<:3ds:1036763036674961468>"
        case "switch":
            return "<:NintendoSwitch:1036762589667020881>"
        case "cafemix":
            return "<:PokemonCafeMix:1036761505074524211>"
        case "pogo":
            return "<:PokemonGo:1036761587698114583>"
        case "home":
            return "<:PokemonHome:1036760555106615427>"
        case "master":
            return "<:PokemonMaster:1036761429145030656>"
        case "shuffle":
            return "<:PokemonShuffle:1036761953323974656>"
        case "sleep":
            return "<:sleep:1135578783454343190>"
        case "unite":
            return "<:unite:1137360033621999726>"
        case _:
            return "❓"


def get_brand_icon(brand: str) -> str:
    match brand:
        case "Amiibo":
            return "<:amiibo:1054416940673802250>"
        case "Annaki":
            return "<:aroz:1054418169625837648>"
        case "Barazushi":
            return "<:alpaj:1054418812784627775>"
        case "Cuttlegear":
            return "<:macalamar:1054419333125771395>"
        case "Emberz":
            return "<:apex:1054420011428614234>"
        case "Enperry":
            return "<:dux:1054421119546966146>"
        case "Firefin":
            return "<:friture:1054421546942353521>"
        case "Forge":
            return "<:focus:1054421784142811146>"
        case "Grizzco":
            return "<:MOursSA:1054422098656903268>"
        case "Inkline":
            return "<:abysma:1054422423686094908>"
        case "Krak-On":
            return "<:krakers:1054423077242536056>"
        case "Rockenberg":
            return "<:iormungand:1054423374836813906>"
        case "Skalop":
            return "<:jack:1054423836885516348>"
        case "Splash Mob":
            return "<:gedeon:1054424146886537286>"
        case "SquidForce":
            return "<:kalamarus_rex:1054424465632657428>"
        case "Takoroka":
            return "<:cubic:1054424706331201546>"
        case "Tentatek":
            return "<:oculr:1054425072582021232>"
        case "Toni Kensa":
            return "<:thony_k:1054425413784453252>"
        case "Zekko":
            return "<:ezko:1054425882858639410>"
        case "Zink":
            return "<:leviathus:1054426036093341839>"
        case _:
            return "<:no_brand:1054426078090887228>"


def get_ability_icon(ability: str) -> str:
    match ability:
        case "Ink Saver (Main)":
            return "<:InkSaverMain:1055107474836959312>"
        case "Ink Saver (Sub)":
            return "<:InkSaverSub:1055107735974326383>"
        case "Ink Recovery Up":
            return "<:InkRecoveryUp:1055108019500879923>"
        case "Run Speed Up":
            return "<:RunSpeedUp:1055108788044173403>"
        case "Swim Speed Up":
            return "<:SwimSpeedUp:1055109232288092250>"
        case "Special Charge Up":
            return "<:SpecialChargeUp:1055109455366340662>"
        case "Special Saver":
            return "<:SpecialSaver:1055109643237589002>"
        case "Special Power Up":
            return "<:SpecialPowerUp:1055109836456603679>"
        case "Quick Respawn":
            return "<:QuickRespawn:1055110053100793966>"
        case "Quick Super Jump":
            return "<:QuickSuperJump:1055111046894993478>"
        case "Sub Power Up":
            return "<:SubPowerUp:1055111628665925724>"
        case "Ink Resistance Up":
            return "<:InkResistanceUp:1055111932002177104>"
        case "Sub Resistance Up":
            return "<:SubResistanceUp:1055112154388373625>"
        case "Intensify Action":
            return "<:IntensifyAction:1055112559214202912>"
        case "Opening Gambit":
            return "<:OpeningGambit:1055112929722241035>"
        case "Last-Ditch Effort":
            return "<:LastDitchEffort:1055113163701489734>"
        case "Tenacity":
            return "<:Tenacity:1055113369436299354>"
        case "Comeback":
            return "<:Comeback:1055113723594936412>"
        case "Ninja Squid":
            return "<:NinjaSquid:1055113913429151794>"
        case "Haunt":
            return "<:Haunt:1055114224541646908>"
        case "Thermal Ink":
            return "<:ThermalInk:1055114371845595206>"
        case "Respawn Punisher":
            return "<:RespawnPunisher:1055114509305520170>"
        case "Ability Doubler":
            return "<:AbilityDoubler:1055114687584407573>"
        case "Stealth Jump":
            return "<:StealthJump:1055114866878332979>"
        case "Object Shredder":
            return "<:ObjectShredder:1055115003683938326>"
        case "Drop Roller":
            return "<:DropRoller:1055115219719958598>"
        case "Bomb Defense Up DX":
            return "<:BombDefenseUpDX:1055115563531251782>"
        case "Main Power Up":
            return "<:MainPowerUp:1055115725188120586>"
        case "Unknown":
            return "<:Unknown:1055115944965455882>"
        case _:
            return "❓"
